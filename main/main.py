from functions import *
#from get_wplist import WPlist
import Robot as rob
import numpy as np
import math
import os


# RF24 imports
import sys
import time
import struct
from RF24 import RF24, RF24_PA_LOW


capX = 352
capY = 288
coeff = 1

# threshold for change to next WP
epsilonWP = 0.01

# écrire en dur ici après avoir lancé get_wplist.py sur un PC
WPlist = [[270, 210],[270, 210]]    #, [316, 232], [316, 233], [317, 233]]

# init WPManager
WPManager = rob.WPManager(WPlist, epsilonWP)


# initialisation des variables de calcul
vConsign = 0.0
thetaRef = 0.0
#omegaRef = 0.0 # apparemment pas utile ici
OK = True


currentframe = 0
# créer un dossiers pour stocker les frames s'il n'existe pas 
if not os.path.exists('frames'):
    os.mkdir('frames')


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

"""
name = "./output.csv"
with open(name, "w") as o:  
    print('XP, YP, XC, YC, XR, YR', o)
    o.close()
"""

# initialisation de la correction en position

# gains des correcteurs (orientation > vitesse)
kp_theta = 0.01
kp_v     = 0.0001

# caractéristiques du robot
d = 0.135
r = 0.035
# TODO : mesurer la vitesse de rotation maximale du moteur (en m / s)
w_max = 200
robot = rob.Robot(d, r, - w_max, w_max)
wD_ref = 0
wG_ref = 0

errorSumV = 0
errorSumw = 0

# initialisation de la radio
radio = RF24(22,0)
if not radio.begin():
    raise RuntimeError("radio hardware is not responding")
address = [b"1Node", b"2Node"]
radio_number = 1
radio.setPALevel(RF24_PA_LOW)
radio.openWritingPipe(address[radio_number])
radio.payloadSize = len(struct.pack("ii", wD_ref, wG_ref))
radio.stopListening()


theta_sum = 0
n_iteration = 1

kVp = 0.005
kwp = 0.1

kVi = 0.00001
kwi = 0.001

while (1):
    get_coord(cap, int(capX/coeff), int(capY/coeff), robot, currentframe)

    # on passe au noeud suivant si le noeud de référence est atteint
    if WPManager.distanceToCurrentWP(robot.x, robot.y) <= epsilonWP :
        print("switch to next WP")
        WPManager.switchToNextWP()
    
    robot.theta     = np.arctan2(robot.y - robot.py, robot.x - robot.px)
    robot.theta_ref = np.arctan2(WPManager.yr - robot.y, WPManager.xr - robot.x)


    theta_sum = theta_sum + robot.theta
    robot.theta = theta_sum / n_iteration
    n_iteration += 1


    # calcul des erreurs
    errorV = (np.sqrt((WPManager.xr - robot.x) ** 2 + (WPManager.yr - robot.y) ** 2))
    errorw = (robot.theta_ref - robot.theta)

    # correction proportionnelle
    corrVp          = kVp * errorV
    corrwp          = kwp * errorw

    # correction intégrale
    errorSumV       += errorV
    errorSumw       += errorw

    corrVi          = kVi * errorSumV
    corrwi          = kwi * errorSumw

    robot.V         = corrVp + corrVi
    robot.w         = corrwp + corrwi
    
    robot_wD_ref    = ((2 * robot.V) + (robot.w * d)) / (2 * r)
    robot.wG_ref    = ((2 * robot.V) - (robot.w * d)) / (2 * r)

    robot.wD_ref    = int(robot_wD_ref)
    robot.wG_ref    = int(robot.wG_ref)

    debug2(robot, WPManager)

    buff = struct.pack("ii", robot.wD_ref, robot.wG_ref)
    result = radio.write(buff)
    
    robot.px = robot.x
    robot.py = robot.y
