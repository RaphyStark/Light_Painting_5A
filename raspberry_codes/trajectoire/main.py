from functions import *
import Robot as rob
import numpy as np
import math
import os

# RF24 imports
import sys
import time
import struct
#from RF24 import RF24, RF24_PA_LOW

# PROBLEME
# Si on resize à 160 90 la caméra ne voit pas à plus d'1 mètre
# Resize à plus que 160 90 (200 200 par exemple) peut résoudre le problème
# mais implique un temps de path build plus long
# l'autre solution est de jouer sur les paramètres (blur etc.)


# main step 1 : get camera dimensions
#cap, capX, capY = get_cam_dimensions()
"""
# 1.1. Ouvrir le flux video
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
"""

#capX = 352
#capY = 288
capX = 160
capY = 90
coeff = 1


# main step 2 : resize light painting image dimensions
img = set_draw_dimensions(int(capX/coeff), int(capY/coeff))


# main step 3 : generate carte
carte = generate_carte(img, int(capX/coeff), int(capY/coeff))


# main step 4.A : get start node from click
node_x, node_y = get_nodes(carte)
start = (int(capX/coeff) * node_y)  + node_x
startNode = carte.graph.listOfNodes[start]


# main step 4.B : get goal node from click
node_x, node_y = get_nodes(carte)
goal = (int(capX/coeff) * node_y)  + node_x
goalNode = carte.graph.listOfNodes[goal]


# main step 5 : generate path
#path = generate_path(carte, start, goal)

closedList, successFlag = carte.AStarFindPath(start, goal, epsilon=0.1)
if (successFlag==True):
    print("building the path...")
    path, lenpath = carte.builtPath(closedList)
    #print("path : " + str(path))
    print("plotting the path...")
    carte.plotPathOnMap(path, 1)
    plt.show()
else :
    print("error generating waypoint")
    exit()

print("please close this final plot")
plt.close('all')


# main step 6 : generate WPlist
WPlist = WP_generator(carte, path)

# Main step 3 : initialize a robot
d = 0.135    # en m
r = 0.035     # en m
# TODO : mesurer la vitesse de rotation maximale du moteur (en m / s)
w_max = 200
robot = rob.Robot(0, 0, 0, d, r, - w_max, w_max)



# Main step 5 : initialize a radio
"""
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

uL = 0
uR = 0

radio_number = 0
radio.setPALevel(RF24_PA_LOW)
radio.openWritingPipe(address[radio_number])
radio.payloadSize = len(struct.pack("ii", uL, uR))
radio.stopListening()

"""

# Main step 6 : robot control

# threshold for change to next WP
epsilonWP = 0.01

# init WPManager
WPManager = rob.WPManager(WPlist, epsilonWP)


# gains des correcteurs
kp_v = 0.2    # pour la vitesse de référence
kp_theta = 1.0    # pour l'angle de référence

# initialisation des variables de calcul
vConsign = 0.0
thetaRef = 0.0
#omegaRef = 0.0 # apparemment pas utile ici
OK = True


currentframe = 0
# créer un dossiers pour stocker les frames s'il n'existe pas 
if not os.path.exists('frames'):
    os.mkdir('frames')


cap = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

#while OK is True :


# duration of scenario and time step for numerical integration
t0 = 0.0
tf = 1000.0
dt = 0.01
simu = rob.RobotSimulation(robot, t0, tf, dt)

for t in simu.t: 
    get_coord(cap, int(capX/coeff), int(capY/coeff), robot, currentframe)

    # on vérifie qu'on a pas déjà atteint le noeud de référence courant
    if WPManager.distanceToCurrentWP(robot.x, robot.y) <= epsilonWP :
        print("switch to next WP")
        WPManager.switchToNextWP()

    # 10. calcul de robot.theta (theta)
    delta_theta = np.arctan2(robot.y - robot.py, robot.x - robot.px)
    robot.theta = robot.theta + delta_theta

    # calcul de thetaRef (reference en orientation)
    thetaRef = np.arctan2(WPManager.yr - robot.y, WPManager.xr - robot.x)
    if math.fabs(robot.theta-thetaRef)>math.pi:
        thetaRef = thetaRef + math.copysign(2*math.pi,robot.theta)        

    # calcul de l'angle de consigne thetaConsign
    thetaConsign = kp_theta * (thetaRef - robot.theta)

    # calcul de vConsign (reference en vitesse)
    vConsign = kp_v * np.sqrt((WPManager.xr - robot.x)**2 + (WPManager.yr - robot.y)**2)

    # 12. Calculer wD et wG en fonction de vRef et thetaRef
    robot.wD = (2 * vConsign) - (thetaRef * d) / (2 * r)
    robot.wG = (2 * vConsign) + (thetaRef * d) / (2 * r)

    # 13. Calculer uD et uL en fonction de wD et wG
    uR = map(robot.wD, robot.w_min, robot.w_max, -200, 200)
    uL = map(robot.wG, robot.w_min, robot.w_max, -200, 200)


    print("current position :")
    print("robotX = " + str(robot.x))
    print("robotY = " + str(robot.y))
    print("next x " + str(WPManager.xr))
    print("next y " + str(WPManager.yr))
    print("robottheta = " + str(robot.theta))
    print()
    print()
    print()

    """
    # 14. Envoyer uD et uG au robot
    while (success == False) :
        buffer = struct.pack("ii", uL, uR)
        result = radio.write(buffer)
        if result:
            #print("OK")
            success = True
    """

    robot.px = robot.x
    robot.py = robot.y


# close all figures
#plt.close("all")