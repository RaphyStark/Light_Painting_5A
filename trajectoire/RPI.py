# -*- coding: utf-8 -*-

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


class Coord():
    def __init__(self):
        self.x = 0
        self.y = 0

def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def on_move(event):
    # get the x and y pixel coords
    x, y = event.x, event.y
    if event.inaxes:
        ax = event.inaxes  # the axes instance

def on_click(event):
    if event.button is MouseButton.LEFT:
        coord.x = event.xdata
        coord.y = event.ydata
        plt.disconnect(binding_id)
        plt.close()


def send_buffer(buffer, payload, failures, SENT):
        start_timer = time.monotonic_ns()  # start timer
        result = radio.write(buffer)
        end_timer = time.monotonic_ns()  # end timer
        if not result:
            print("Transmission failed or timed out")
            failures += 1
        else:
            print(
                "Transmission successful! Time to Transmit: "
                "{} us. Sent: {}".format(
                    (end_timer - start_timer) / 1000,
                    payload
                )
            )
            SENT = True


def master(payload1, payload2):
    """Transmits an incrementing float every second"""
    radio.stopListening()  # put radio in TX mode
    failures = 0
    SENT = False
    SENT1 = False
    SENT2 = False
    while (SENT == False or failures < 6) :
        # use struct.pack() to packet your data into the payload
        # "<f" means a single little endian (4 byte) float value.
        buffer = struct.pack("<f", payload1)
        send_buffer(buffer, payload1, failures, SENT1)
        buffer = struct.pack("<f", payload2)
        send_buffer(buffer, payload2, failures, SENT2)
        time.sleep(1)
        if (SENT1 == True and SENT2 == True) :
            SENT = True
    else : 
        if failures >= 6 :
            print(failures, "failures detected. Leaving TX role.")
            exit()


# VARIABLES GLOABLES
LOGITECH_RESIZE_HEIGHT = 90
LOGITECH_RESIZE_WIDTH = 160
MACBOOK_CAM_RESIZE_HEIGHT = 288
MACBOOK_CAM_RESIZE_WIDTH = 352
capX = 0
capY = 0
name = "spirale.jpg"


# 1. Get VideoCapture dimensions

# 1.1. Ouvrir le flux video
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 1.2. Récupérer les dimensions dans capX et capY
capX = cap.get(cv.CAP_PROP_FRAME_WIDTH)
capY = cap.get(cv.CAP_PROP_FRAME_HEIGHT)





# 2. Set VideoCapture dimensions to (capX = 160, capY = 90)

# 2.0. On vérifie les valeurs des variables avant modification
# print("capX = " + str(capX))
# print("capY = " + str(capY))

# 2.1. Set dimensions
cap.set(cv.CAP_PROP_FRAME_WIDTH, LOGITECH_RESIZE_WIDTH)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, LOGITECH_RESIZE_HEIGHT)

# 2.2. On récupère les nouvelles valeurs dans capX et capY
capX = cap.get(cv.CAP_PROP_FRAME_WIDTH)#160
capY = cap.get(cv.CAP_PROP_FRAME_HEIGHT)#90

# 2.3. On vérifie les valeurs des variables après modification
# print("capX = " + str(capX))
# print("capY = " + str(capY))

# 2.4. On vérifie la possibilité de prendre une capture dans le flux
success, frame = cap.read()
if success is True :
    capY = int(frame.shape[0])
    capX = int(frame.shape[1])
else :
    print("Problem capturing a frame")
    exit()

# 2.5. On affiche le flux vidéo dans une fenêtre OpenCV
'''
while success is True :
    success, frame = cap.read()
    if not success :
        print("cap read not successed")
        break    
    windowName = "frame by frame"
    cv.namedWindow(windowName)
    cv.imshow(windowName, frame)
    k = cv.waitKey(1) & 0xff
    if (k == 27) : 
        success = False
cv.destroyWindow(windowName)
'''





# 3. Set draw img at VideoCapture new dimensions

# 3.1. Import image
img = cv.imread(name)

# 3.2. Resize image at VideoCapture dimensions / 10
capX = round(capX/10)
capY = round(capY/10)
img = cv.resize(img, (capX, capY))

# 3.3. Check values
print("capX = " + str(capX) + " and imgX = " + str(img.shape[1]))
print("capY = " + str(capY) + " and imgY = " + str(img.shape[0]))





# 4. Générer une grille d'occupation à partir de l'image

# 4.1. Passage en nuances de gris
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 4.2. Passage en binaire
img = cv.threshold(img, 200, 1, 0)
img = img[1]

# 4.3. Inversion des obstacles et des cases libres
for i in range(len(img)):
    for j in range (len(img[0])) :
        if img[i][j] == 0:
            img[i][j] = 1
        else :
            img[i][j] = 0

# 4.4. Chargement du tableau occupancyGrid
wait=[]
list=[]
for y in range(0, capX):
    for x in range(0, capY):
        wait.append(img[x][y])
    list.append(wait)
    wait=[]
list = np.array(list)
occupancyGrid = list





# 5. Sélectionner les noeuds de départ et d'arrivée sur la carte

# 5.1. Création de la carte (objet Map)
adjacency = 4
carte = AStar.Map(capX, capY, adjacency)
carte.initCoordinates()
carte.loadOccupancy(occupancyGrid)
carte.generateGraph()

# 5.2. Afficher une première fois la carte pour cliquer sur le noeud de départ
fig1 = plt.figure()
carte.plot(1)
coord = Coord()
binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)
plt.show()
start_node_x = round(coord.x)
start_node_y = round(coord.y)

# 5.3. Afficher une seconde fois la carte pour cliquer sur le noeud d'arrivée
fig1 = plt.figure()
carte.plot(1)
coord = Coord()
binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)
plt.show()
goal_node_x = round(coord.x)
goal_node_y = round(coord.y)





# 6. Générer les numéros des noeuds de départ et d'arrivée

# 6.1. Noeud de départ :
start_node_no   = (capX * start_node_y)  + start_node_x
startNode = carte.graph.listOfNodes[start_node_no]

# 6.2. Noeud d'arrivée :
goal_node_no    = (capX * goal_node_y)  + goal_node_x
goalNode = carte.graph.listOfNodes[goal_node_no]

# 6.3. Affichage des noeuds
# print("start node = " + str(startNode))
# print("goal node = " + str(goalNode))





# 7. Générer un chemin entre les deux noeuds avec l'algorithme A*
closedList, successFlag = carte.AStarFindPath(start_node_no, goal_node_no, epsilon=0.1)
if (successFlag==True):
    path, lenpath = carte.builtPath(closedList)
    carte.plotPathOnMap(path, 1)
    plt.show()
    #carte.plotExploredTree(closedList, 2)



# 8. Générer une liste de coordonnées de points de passage
WPlist = []
for i in range(len(path)):
    current_node = path[i]
    coord = []
    coord.append(carte.graph.listOfNodes[current_node].x)
    coord.append(carte.graph.listOfNodes[current_node].y)
    WPlist.append(coord)




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


# print("robotX = " + str(robotX))
# print("robotY = " + str(robotY))
# robotNodeNo = (capX * robotY) + robotX



# 10. Définir un objet robot avec la pose initiale
# TODO : vérifier les dimensions
# unité S.I. -> mètres
d = 0.135    # en m
r = 0.035     # en m
# TODO : mesurer la vitesse de rotation maximale du moteur (en m / s)
w_max = 200

robot = rob.Robot(robotX, robotY, robotTheta0, d, r, - w_max, w_max)




# définir un objet radio pour la communication
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


# 11. Calculer V et Omega en fonction de la pose et du noeud suivant



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

# radio.powerDown()