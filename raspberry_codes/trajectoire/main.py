from functions import *
from robot_localisation import get_coord

import matplotlib.pyplot as plt
import Robot as rob
import cv2 as cv
import numpy as np
import math


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# Main step 1 : get camera dimensions
cap, capX, capY = get_cam_dimensions()

# resize light painting image dimensions


# Main step 2 : generate WP
carte, start, goal = get_nodes(capX, capY)

# build map
path = generate_path(carte, start, goal)

WPlist = WP_generator(carte, path)

# Main step 3 : initialize a robot
d = 0.135    # en m
r = 0.035     # en m
# TODO : mesurer la vitesse de rotation maximale du moteur (en m / s)
w_max = 200
robot = rob.Robot(0, 0, 0, d, r, - w_max, w_max)

# Main step 4 : get robot initial coordinates
robot.x, robot.y = get_coord(cap, capX, capY)

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


while OK is True :
    
    robot.x, robot.y = get_coord(cap, capX, capY)

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
plt.close("all")