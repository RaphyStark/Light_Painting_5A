# RF24 imports
import sys
import argparse
import time
import struct
from RF24 import RF24, RF24_PA_LOW

# library imports
from typing import Mapping
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import math

# personal functions import
from functions import *

# robotic libraries import
import Robot as rob
import Timer as tmr
import AStar

def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)







# TD1 Génération de trajectoire

# dimensions of the map
dimX = 20
dimY = 10

# occupancy grid
occupancyGrid = np.zeros([dimX, dimY])
occupancyGrid[2:4,2:4]=1
occupancyGrid[6,1:3]=1
occupancyGrid[4:7,3]=1
occupancyGrid[8:10,2:6]=1
occupancyGrid[4:6,6:8]=1
occupancyGrid[6,5:7]=1
occupancyGrid[10:12,7:10]=1
occupancyGrid[11,0:3]=1
occupancyGrid[11:15,4:6]=1
occupancyGrid[13:15,2:5]=1
occupancyGrid[15,3:5]=1
occupancyGrid[16:18,3]=1
occupancyGrid[18:20,5]=1
occupancyGrid[14,7:9]=1
occupancyGrid[16,7:10]=1


# max adjacency degree
adjacency = 8

# create and plot map
carte = AStar.Map(dimX,dimY, adjacency)
carte.initCoordinates()
carte.loadOccupancy(occupancyGrid)
carte.generateGraph()

# weighted A* algorithm
startNodeNo = 0
goalNodeNo = 199
closedList, successFlag = carte.AStarFindPath(startNodeNo,goalNodeNo, epsilon=1.0)

if (successFlag==True):
    path, lenpath = carte.builtPath(closedList)
    carte.plotPathOnMap(path, 2)
    carte.plotExploredTree(closedList, 3)
    # print("trajectoire : " + str(path))


# list of way points: list of [x coord, y coord]
WPlist = []
for i in range(len(path)):
    current_node = path[i]
    coord = []
    coord.append(carte.graph.listOfNodes[current_node].x)
    coord.append(carte.graph.listOfNodes[current_node].y)
    WPlist.append(coord)









# 1.1. Ouvrir le flux video
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()




# 9. Obtenir les coordonnées (x,y) du robot par la caméra
#while True :
success, frame = cap.read()
# currentframe = 0
if not success :
    print("cap read not successed")   
gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
gray_image = cv.blur(gray_image, (5,3))
success,thresh = cv.threshold(gray_image,127,255,0)
if not success :
    print("threshold not successed")
# find contours in the binary image
contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)
for c in contours:
    # calculate moments for each contour
    M = cv.moments(c)
    # calculate x,y coordinate of center 
    robotX = 0
    robotY = 0       
    if (M["m00"] != 0) :
        robotX = int(M["m10"] / M["m00"])    
        robotY = int(M["m01"] / M["m00"])
        # Conversion dans le format de l'image
        robotX = int(robotX)
        robotY = int(robotY)
        robotTheta0 = 0
        # TODO : calcul de robotTheta0 
        #   soit en mettant une LED à l'avant et à l'arrière du robot et en calculant l'angle entre les deux
        #   soit en placant le robot à un angle donné au départ (moins recommandé car problème d'écart d'angle sur le long terme...)
        #   soit une centrale inertielle




# 10. Définir un objet robot avec la pose initiale
# TODO : vérifier les dimensions
# unité S.I. -> mètres
d = 0.135    # en m
r = 0.035     # en m
# TODO : mesurer la vitesse de rotation maximale du moteur (en m / s)
w_max = 200

robot = rob.Robot(robotX, robotY, robotTheta0, d, r, - w_max, w_max)




# 11. définir un objet radio pour la communication
radio = RF24(22,0)
# initialize the nRF24L01 on the spi bus
if not radio.begin():
    raise RuntimeError("radio hardware is not responding")
# For this example, we will use different addresses
# An address need to be a buffer protocol object (bytearray)
address = [b"1Node", b"2Node"]
# It is very helpful to think of an address as a path instead of as
# an identifying device destination
print(sys.argv[0])  # print example name
# to use different addresses on a pair of radios, we need a variable to
# uniquely identify which address this radio will use to transmit
# 0 uses address[0] to transmit, 1 uses address[1] to transmit
radio_number = 1  # force master



###### Mise en place de la boucle de contrôle ######

# position control loop timer
positionCtrlPeriod = 0.2
timerPositionCtrl = tmr.Timer(positionCtrlPeriod)

# orientation control loop timer
orientationCtrlPeriod = 0.05
timerOrientationCtrl = tmr.Timer(orientationCtrlPeriod)

# threshold for change to next WP
epsilonWP = 0.01

# init WPManager
WPManager = rob.WPManager(WPlist, epsilonWP)

# duration of scenario and time step for numerical integration
t0 = 0.0
tf = 5000.0
dt = 0.01
simu = rob.RobotSimulation(robot, t0, tf, dt)

# gains des correcteurs
kp_v = 0.2    # pour la vitesse de référence
kp_theta = 1.0    # pour l'angle de référence

# initialisation des variables de calcul
vConsign = 0.0
thetaRef = 0.0
#omegaRef = 0.0 # apparemment pas utile ici
###### Fin de la mise en place ######



###### Début de la boucle de contrôle ######
# loop on simulation time
for t in simu.t: 


    # on vérifie qu'on a pas déjà atteint le noeud de référence courant
    #if WPManager.distanceToCurrentWP(robot.x, robot.y) <= epsilonWP :
    #    WPManager.switchToNextWP()

        # 10. calcul de thetaRobot
        robot.theta = np.arctan2(robot.y - robot.py, robot.x - robot.px)

        # calcul de thetaRef (reference en orientation)
        thetaRef = np.arctan2(WPManager.yr - robot.y, WPManager.xr - robot.x)
        if math.fabs(robot.theta-thetaRef)>math.pi:
            thetaRef = thetaRef + math.copysign(2*math.pi,robot.theta)        

        # calcul de l'angle de consigne thetaConsign
        #if timerOrientationCtrl.isEllapsed(t):
        thetaConsign = kp_theta * (thetaRef - robot.theta)

        # calcul de vConsign (reference en vitesse)
        vConsign = kp_v * np.sqrt((WPManager.xr - robot.x)**2 + (WPManager.yr - robot.y)**2)


        # 12. Calculer wD et wG en fonction de vRef et thetaRef
        robot.wD = (2 * vConsign) - (thetaRef * d) / (2 * r)
        robot.wG = (2 * vConsign) + (thetaRef * d) / (2 * r)

        # 13. Calculer uD et uL en fonction de wD et wD
        uD = map(robot.wD, robot.w_min, robot.w_max, -200, 200)
        uG = map(robot.wG, robot.w_min, robot.w_max, -200, 200)

        # 14. Envoyer uD et uG au robot
        radio.master(uG, uD)


        # fonction de mise à jour de la pose du robot (robot.x, robot.y, robot.theta)
        # TODO : updatePose()

        # close all figures
        plt.close("all")

        # generate plots
        simu.plotXY(1, -1, capX, -1, capY)
        simu.plotXYTheta(2)
        simu.plotVOmega(3)
        carte.plotPathOnMap(path, 4)
        plt.show()

    ###### Fin de la boucle de contrôle ######



