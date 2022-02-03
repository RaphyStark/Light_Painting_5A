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




# main step 1 : get camera dimensions
#cap, capX, capY = get_cam_dimensions()


capX = 352
capY = 288
coeff = 1


# Main step 3 : initialize a robot
d = 0.135    # en m
r = 0.035     # en m
# TODO : mesurer la vitesse de rotation maximale du moteur (en m / s)
w_max = 200
robot = rob.Robot(0, 0, 0, d, r, - w_max, w_max)





# Main step 5 : initialize a radio

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

radio_number = 1
radio.setPALevel(RF24_PA_LOW)
radio.openWritingPipe(address[radio_number])
radio.payloadSize = len(struct.pack("ii", uL, uR))
radio.stopListening()



# Main step 6 : robot control

# threshold for change to next WP
epsilonWP = 0.01

# écrire en dur ici après avoir lancé get_wplist.py sur un PC
WPlist = [[316, 231], [316, 232], [316, 233], [317, 233]]

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


cap = cv.VideoCapture(0)
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

    """
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
    #success = False
    # 14. Envoyer uD et uG au robot
    #while (success == False) :
    
    buff = struct.pack("ii", uL, uR)
    result = radio.write(buff)
    if result:
        print("OK")
        #success = True
    else:
        print("failed to send")
    
    robot.px = robot.x
    robot.py = robot.y


# close all figures
#plt.close("all")
