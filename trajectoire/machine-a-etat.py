# library imports
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



# VARIABLES GLOABLES

LOGITECH_RESIZE_HEIGHT = 90
LOGITECH_RESIZE_WIDTH = 160

MACBOOK_CAM_RESIZE_HEIGHT = 288
MACBOOK_CAM_RESIZE_WIDTH = 352

capX = 0
capY = 0

name = "spirale.jpg"





# 1. Get VideoCapture dimensions

# 1.1. Ouvrir le flux vidéo
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

print("robotX = " + str(robotX))
print("robotY = " + str(robotY))
# robotNodeNo = (capX * robotY) + robotX





# 10. Obtenir l'orientation theta du robot
robotTheta = 0 # TODO





# 11. Calculer V et Omega en fonction de la pose et du noeud suivant
# 11.0. Création des objets et des variables
robot = rob.Robot(robotX, robotY, robotTheta)

# 11.1. position control loop timer
positionCtrlPeriod = 0.2
timerPositionCtrl = tmr.Timer(positionCtrlPeriod)

# 11.2. orientation control loop timer
orientationCtrlPeriod = 0.05
timerOrientationCtrl = tmr.Timer(orientationCtrlPeriod)

# 11.3. threshold for change to next WP
epsilonWP = 0.01

# 11.4. init WPManager
WPManager = rob.WPManager(WPlist, epsilonWP)

# 11.5. duration of scenario and time step for numerical integration
t0 = 0.0
tf = 5000.0
dt = 0.01
simu = rob.RobotSimulation(robot, t0, tf, dt)

# initialize control inputs
Vr = 0.0
thetar = 0.0
omegar = 0.0

# loop on simulation time
for t in simu.t: 

    # WP navigation: switching condition to next WP of the list
    if WPManager.distanceToCurrentWP(robot.x, robot.y) <= epsilonWP :
        WPManager.switchToNextWP()

    k1 = 0.2
    k2 = 1.0

    # position control loop
    if timerPositionCtrl.isEllapsed(t):

        # calcul de Vr (reference vitesse)
        Vr = k1 * np.sqrt((WPManager.xr - robot.x)**2 + (WPManager.yr - robot.y)**2)

        # calcul de thetar (reference orientation)
        thetar = np.arctan2(WPManager.yr - robot.y,WPManager.xr - robot.x)

        if math.fabs(robot.theta-thetar)>math.pi:
            thetar = thetar + math.copysign(2*math.pi,robot.theta)        


    # orientation control loop
    if timerOrientationCtrl.isEllapsed(t):
        # angular velocity control input        
        omegar = k2 * (thetar - robot.theta)

    # apply control inputs to robot
    
    wD = 0
    wG = 0
    r = 3.5     # rayon des roues en cm
    d = 13.5    # distance entre les roue en cm

    VecCommand = [[Vr], [omegar]]       # 1,2
    VecA = [[r/2, r/2], [r/d, -r/d]]    # 2,2
    VecMot = [wD, wG]                   # 1,2

    # 1,2   =   1,2     *       2,2

    #                                               [r/2         r/2]
    #   [wD   wG]    =      [Vr     OmegaR]     *                        
    #                                               [r/d        -r/d]


    VecMot = (VecCommand * VecA.reverse()).reverse()

    print("Vec Mot = " + str(VecMot))

    # 12. TODO : Calculer tension moteurs d'après V et Omega
    # 13. TODO : Envoyer les tensions moteurs au robot
    robot.setV(Vr)
    robot.setOmega(omegar)
    
    # integrate motion
    # TODO : attendre un peu et mettre à jour robotX et robotY par la caméra
    robot.integrateMotion(dt)

    # store data to be plotted   
    simu.addData(robot, WPManager, Vr, thetar, omegar)
    
# end of loop on simulation time

# close all figures
plt.close("all")

# generate plots
simu.plotXY(1, -1, capX, -1, capY)
simu.plotXYTheta(2)
simu.plotVOmega(3)
carte.plotPathOnMap(path, 4)
plt.show()

# When everything done, release the capture
cap.release()