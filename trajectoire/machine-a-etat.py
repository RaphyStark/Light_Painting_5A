import cv2 as cv
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import Robot as rob
from numpy.lib.type_check import imag
import AStar
import Timer as tmr
import math

def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)
    return cap


def setup(img_X, img_Y) :
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    #dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    #dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    print(img_X)
    print(img_Y)

    #if (dimX >= img_X and dimY >= img_Y):
    #cap = change_res(cap, img_X, img_Y)
    cap.set(3, img_X)
    cap.set(4, img_Y)
    print(int(cap.get(3))) #cv.CAP_PROP_FRAME_WIDTH
    print(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))


    dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    return cap, dimX, dimY


def read_img():
    success, frame = cap.read()
    if not success :
        print("Can't receive frame (stream end?). Exiting ...")
    return frame


def calc_coord() :

    '''
    # copie du début de la fonction setup()
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    '''

    success, frame = cap.read()

    #currentframe = 0

    # convert the image to grayscale
    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_image = cv.blur(gray_image, (5,3))

    success,thresh = cv.threshold(gray_image,127,255,0)
    if not success :
        print("threshold problem")

    # find contours in the binary image
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)

    for c in contours:
        # calculate moments for each contour
        M = cv.moments(c)

        # calculate x,y coordinate of center        
        if (M["m00"] != 0) :
            X = int(M["m10"] / M["m00"])    
            Y = int(M["m01"] / M["m00"])

        return X, Y


def find_no_from_coord() :
    current_node = 0
    last_node = dimX*dimY - 1

    while (current_node != last_node) :
        if carte.graph.listOfNodes[current_node].x == start_node_x :
            #print("x ok")

            #print(current_node)
            if carte.graph.listOfNodes[current_node].y == start_node_y :
                #print("y ok")
                start_node = current_node
                break
            else : 
                current_node = current_node + 1
        else : 
            #print(current_node)
            current_node = current_node + 1
    
    #print("start node x = " +str(carte.graph.listOfNodes[start_node].x))
    #print("start node y = " +str(carte.graph.listOfNodes[start_node].y))


    return current_node


#name = "spirale.jpg"
name = "rabbit.jpeg"

# 1. Récupération de la dimension du dessin
img = cv.imread(name)
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
img = cv.threshold(img, 253, 1, 0)
img = img[1]
imgY = int(img.shape[0])#/10)
imgX = int(img.shape[1])#/10)
img = cv.resize(img, (imgX, imgY))


# 2. Récupérer la dimension du champ de vision de la caméra
#cap, capX, capY = setup(imgX, imgY)

####
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print(imgX) # 750
print(imgY) # 477

#if (dimX >= img_X and dimY >= img_Y):
#cap = change_res(cap, img_X, img_Y)

cap.set(3, 640)
cap.set(4, 480)

rect, frame = cap.read()

if rect is True :
    print(int(frame.shape[0]))
    print(int(frame.shape[1]))

else :
    print("NON")

#print(int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
#print(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))


#dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
#dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
####

#print(dimX)    # 1280
#print(dimY)    # 720

#print(dimX_cam)    # 1280
#print(dimY_cam)    # 720







'''
# 3. Faire correspondre les dimensions de la carte avec celles de la caméra


# TODO


# Générer une grille d'occupation à partir d'une image
wait=[]
list=[]
for y in range(0, dimX):
    for x in range(0, dimY):
        wait.append(img[x][y])
    list.append(wait)
    wait=[]
list = np.array(list)
occupancyGrid = list




# 3. Création de la carte

adjacency = 8
carte = AStar.Map(dimX, dimY, adjacency)
carte.initCoordinates()
#carte.generateRandObstacles()
carte.loadOccupancy(occupancyGrid)
carte.generateGraph()
#carte.plot(1)
#plt.show()
#print("size adjacency matrix = " + str(carte.graph.adjacencyMatrix))




# 4. Générer les numéros des noeuds de départ et d'arrivée

# dimX = 27
# dimY = 25
# size = dimX*dimY
# lastNodeNo = size - 1
# anyNodeNo = (dimX * anyNode.y)  + anyNode.x


start_node_x = 210
start_node_y = 235

goal_node_x = 115
goal_node_y = 135


start_node_no   = (dimX * start_node_y)  + start_node_x
goal_node_no    = (dimX * goal_node_y)  + goal_node_x



# 6. Générer un chemin entre les deux noeuds avec l'algorithme A*

closedList, successFlag = carte.AStarFindPath(start_node_no, goal_node_no, epsilon=0.5)

if (successFlag==True):
    path, lenpath = carte.builtPath(closedList)
    #carte.plotPathOnMap(path, 1)
    #plt.show()
    # carte.plotExploredTree(closedList, 3)
    # print("trajectoire : " + str(path))

#print("A Star done computing")

# 7. Générer une liste de points de passage
# list of way points: list of [x coord, y coord]
WPlist = []
for i in range(len(path)):
    current_node = path[i]
    coord = []
    coord.append(carte.graph.listOfNodes[current_node].x)
    coord.append(carte.graph.listOfNodes[current_node].y)
    WPlist.append(coord)




# 8. Obtenir les coordonnées du robot grâce au script python de localisation


# initialisation d'un objet robot : pose (x,y,theta)
# theta0 en réel
#(x0, y0) = calc_coord()

theta0 = 0.0
x0 = carte.graph.listOfNodes[start_node_no].x
y0 = carte.graph.listOfNodes[start_node_no].y
robot = rob.Robot(x0, y0, theta0)


# position control loop timer
positionCtrlPeriod = 0.2
timerPositionCtrl = tmr.Timer(positionCtrlPeriod)

# orientation control loop timer
orientationCtrlPeriod = 0.05
timerOrientationCtrl = tmr.Timer(orientationCtrlPeriod)

#threshold for change to next WP
epsilonWP = 0.01

# init WPManager
WPManager = rob.WPManager(WPlist, epsilonWP)

# duration of scenario and time step for numerical integration
t0 = 0.0
tf = 5000.0
dt = 0.01
simu = rob.RobotSimulation(robot, t0, tf, dt)

# initialize control inputs
Vr = 0.0
thetar = 0.0
omegar = 0.0
  
print("start simu")

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

        #thetar_av = thetar
        
        if math.fabs(robot.theta-thetar)>math.pi:
            thetar = thetar + math.copysign(2*math.pi,robot.theta)        

        #thetar_ap = thetar

        #if thetar_av != thetar_ap :
            #print("thetar avant = " + str(thetar_av))
            #print("thetar après = " + str(thetar_ap))

    # orientation control loop
    if timerOrientationCtrl.isEllapsed(t):
        # angular velocity control input        
        omegar = k2 * (thetar - robot.theta)

    # apply control inputs to robot
    robot.setV(Vr)
    robot.setOmega(omegar)
    
    # integrate motion
    robot.integrateMotion(dt)

    # store data to be plotted   
    simu.addData(robot, WPManager, Vr, thetar, omegar)
    
# end of loop on simulation time



# close all figures
plt.close("all")

# generate plots
simu.plotXY(0, -1, 30, -1, 30)
#simu.plotXYTheta(2)
#simu.plotVOmega(3)

carte.plotPathOnMap(path, 1)
plt.show()







# boucle de commande du robot

    # créer une meilleure condition pour la loop 
    # while 

    # WP navigation: switching condition to next WP of the list
    #if WPManager.distanceToCurrentWP(robot.x, robot.y) <= epsilonWP :
    #   WPManager.switchToNextWP()

    # calcul de V et Omega en fonction de la position et du next point



# When everything done, release the capture
#cap.release()

'''















### COMMENTAIRES UTILES OU OBSOLETES ###


#print(dimX)    # 1280
#print(dimY)    # 720



# nombre de colonnes du tableau img
#dimY = len(img[0])

# nombre de lignes
#dimX = len(img)

#               1ere colonne    2eme colonne ...    1280e colonne
# 1ere ligne    occG[0][0] =                            1279
# 2eme ligne                                            
# ...                                                   
# 720                                               occG[719][1279] = 

#dimX = int(dimX)
#dimY = int(dimY)
'''


#print(dimX)    # 1280
#print(dimY)    # 720

#print(img.shape[0])    #890
#print(img.shape[1])    #970


#print(len(img[len(img)-1]))
#print(img[dimY-1][dimX-1])



# img = cv.GaussianBlur(img, (5,5), 3, 3)

# img = cv.Canny(img,170,200, True)




#xf = 12.0
#yf = 12.0
#print("WPManager.xf = " + str(WPManager.xf))
#print("WPManager.yf = " + str(WPManager.yf))





'''


    # print("dimX = {}".format(dimX))
    # print("dimY = {}".format(dimY))