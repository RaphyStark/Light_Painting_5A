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
WPlist = [[316, 231], [316, 232], [316, 233], [317, 233]]

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

#while OK is True :



# initialisation de la correction en position

# gains des correcteurs (orientation > vitesse)
kp_theta = 0.001
kp_v     = 0.0001

# caractéristiques du robot
d = 0.135
r = 0.035
# TODO : mesurer la vitesse de rotation maximale du moteur (en m / s)
w_max = 200
robot = rob.Robot(0, 0, 0, d, r, - w_max, w_max)

# initialisation de la radio
radio = RF24(22,0)
if not radio.begin():
    raise RuntimeError("radio hardware is not responding")
address = [b"1Node", b"2Node"]
radio_number = 1
radio.setPALevel(RF24_PA_LOW)
radio.openWritingPipe(address[radio_number])
radio.payloadSize = len(struct.pack("ff", robot.wD, robot.wG))
radio.stopListening()

while (1):
    get_coord(cap, int(capX/coeff), int(capY/coeff), robot, currentframe)

    # on vérifie qu'on a pas déjà atteint le noeud de référence courant
    if WPManager.distanceToCurrentWP(robot.x, robot.y) <= epsilonWP :
        print("switch to next WP")
        WPManager.switchToNextWP()


    # calcul de V et de la direction de référence theta_ref (cv. cours commande slide 10)

    # 1 : calcul de vConsign (reference en vitesse)
    # attention:
    # ce n'est pas le calcul d'une vitesse mais d'une sortie d'un correcteur P
    # calculée grace au gain et au déplacement par unité de temps (une itération)
    robot.v_consign = kp_v * np.sqrt((WPManager.xr - robot.x)**2 + (WPManager.yr - robot.y)**2)

    # 2 : calcul de theta_ref

    # 2.1 : calcul de robot.theta
    robot.theta = np.arctan2(robot.y - robot.py, robot.x - robot.px)

    # 2.2 : calcul de theta de réference
    robot.theta_ref = np.arctan2(WPManager.yr - robot.y, WPManager.xr - robot.x)
    
    # si la différence entre theta robot et theta ref > 180°
    # on  ajoute ou soustrait 2pi à theta ref selon le signe de theta robot
    # attention : jamais le cas car arctan2 fait déjà un process
    # qui empêche l'angle d'être supérieur à 180°
    # exemple :
    # >>> np.arctan2(0,-3) * 57.29577913
    # 179.9999987965114
    # >>> np.arctan2(-0.000001,-3) * 57.29577913
    # -179.99997969791835
    if math.fabs(robot.theta - robot.theta_ref) > math.pi:
        robot.theta_ref = robot.theta_ref + math.copysign(2*math.pi,robot.theta)        

    # correcteur P sur le theta
    robot.theta_consign = kp_theta * (robot.theta_ref - robot.theta)

    # 12. Calculer wD et wG en fonction de vRef et thetaRef
    robot.wD = (2 * robot.v_consign) - (robot.theta_consign * d) / (2 * r)
    robot.wG = (2 * robot.v_consign) + (robot.theta_consign * d) / (2 * r)

    #robot.wD = robot.wD * 4.55 * 1440 * 0.15
    #robot.wG = robot.wG * 4.55 * 1440 * 0.15

    debug(robot, WPManager)

    buff = struct.pack("ff", robot.wD, robot.wG)
    result = radio.write(buff)
    
    robot.px = robot.x
    robot.py = robot.y