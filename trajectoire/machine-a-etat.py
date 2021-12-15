import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton

import AStar
#import Robot as rob
#import Timer as tmr
#import matplotlib.patches as patches
#from numpy.lib.type_check import imag
#import math



name = "spirale.jpg"


# explications sur certaines parties du code
# dimX = 27
# dimY = 25
# size = dimX*dimY
# lastNodeNo = size - 1
# anyNodeNo = (dimX * anyNode.y)  + anyNode.x


# eps = 1 : A* calssique
# eps = 0 : dijskra
# eps compris entre 0 et 1 : A* pondéré en proba
# eps > 1 : chemin de plus en plus court


# trajecto 9
# appeler le code de Faly (fonction calc_coord())
# convertir les coordonnées du pixel lumineux en noeud (à un facteur d'échelle près)
# 3. Faire correspondre les dimensions de la carte avec celles de la caméra



class Coord():
    def __init__(self):
        self.x = 0
        self.y = 0

def onclick(event):
    c_x = event.x
    c_y = event.y
    print(c_x)
    print(c_y)
    return c_x,c_y

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

    print(int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

    #if (dimX >= img_X and dimY >= img_Y):
    #cap = change_res(cap, img_X, img_Y)
    cap.set(3, img_X)
    cap.set(4, img_Y)

    print(int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
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
        if (M["m00"] != 0) :
            X = int(M["m10"] / M["m00"])    
            Y = int(M["m01"] / M["m00"])
        return X, Y
'''
def find_no_from_coord(dimX, dimY) :
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
'''
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


# 1. Récupérer la dimension du champ de vision de la caméra
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# LOGITECH
# 90,160
# 288, 352
# 480, 640
# 600, 800
# 896, 1600
# 1080,1920



# MACBOOK_CAM_ORIGINAL_HEIGHT = 720
# MACBOOK_CAM_ORIGINAL_WIDTH = 1280

# LOGITECH_CAM_ORIGINAL_HEIGHT = 1080
# LOGITECH_CAM_ORIGINAL_WIDTH = 1920

# LOGITECH_RESIZE_HEIGHT = 90
# LOGITECH_RESIZE_WIDTH = 160

# MACBOOK_CAM_RESIZE_HEIGHT = 288
# MACBOOK_CAM_RESIZE_WIDTH = 352

#cap.set(cv.CAP_PROP_FRAME_WIDTH, 100)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 100)

# frame.shape[0] # HEIGHT
# frame.shape[1] # WIDTH

success, frame = cap.read()

capX = 0
capY = 0

if success is True :
    capY = int(frame.shape[0])
    capX = int(frame.shape[1])

else :
    print("Problem capturing a frame")
    exit()


# 2. Redimmensionner l'image en fonction de la dimension de la caméra
img = cv.imread(name)
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
capX = int(capX/10)
capY = int(capY/10)
#img = cv.resize(img, (capX, capY))


# 3. Passage de l'image en binaire
img = cv.threshold(img, 200, 1, 0)
img = img[1]

# Inversion des obstacles en cases
for i in range(len(img)):
    for j in range (len(img[0])) :
        if img[i][j] == 0:
            img[i][j] = 1
        else :
            img[i][j] = 0

# 4. Générer une grille d'occupation à partir d'un tableau binaire de l'image
wait=[]
list=[]
for y in range(0, capX):
    for x in range(0, capY):
        wait.append(img[x][y])
    list.append(wait)
    wait=[]
list = np.array(list)
occupancyGrid = list

# 5. Création de la carte
adjacency = 4
carte = AStar.Map(capX, capY, adjacency)
carte.initCoordinates()
#carte.generateRandObstacles()
carte.loadOccupancy(occupancyGrid)
#print("go gener")
carte.generateGraph()
#print("done gener")
fig1 = plt.figure(1)
carte.plot(1)
coord = Coord()
binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)
plt.show()
start_node_x = round(coord.x)
start_node_y = round(coord.y)
#print("start x = " + str(coord.x))
#print("start y = " + str(coord.y))
coord = Coord()
binding_id = plt.connect('motion_notify_event', on_move)
plt.connect('button_press_event', on_click)
fig1 = plt.figure(1)
carte.plot(1)
plt.show()
goal_node_x = round(coord.x)
goal_node_y = round(coord.y)
#print("goal x = " + str(coord.x))
#print("goal y = " + str(coord.y))


# 6. Génération du path en fonction des noeuds de départ et d'arrivée
start_node_no   = (capX * start_node_y)  + start_node_x
goal_node_no    = (capX * goal_node_y)  + goal_node_x


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


# TODO : récupérer WPlist dans un fichier de sauvegarde



# 9. Obtenir les coordonnées du robot grâce au script python de localisation
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


print("robotX = " + str(robotX))
print("robotY = " + str(robotY))


robotNodeNo = (capX * robotY) + robotX



# initialisation d'un objet robot : pose (x,y,theta)
# theta0 en réel
#(x0, y0) = calc_coord()

theta0 = 0.0
x0 = carte.graph.listOfNodes[robotNodeNo].x
y0 = carte.graph.listOfNodes[robotNodeNo].y


print("x0 = " + str(x0))
print("y0 = " + str(y0))




'''
#robot = rob.Robot(x0, y0, theta0)


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



'''

# When everything done, release the capture
cap.release()









### COMMENTAIRES UTILES OU OBSOLETES ###
#source_window = 'resize'
#cv.namedWindow(source_window)
#cv.imshow(source_window, img)
#cv.waitKey()


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

# print("dimX = {}".format(dimX))
# print("dimY = {}".format(dimY))

# print(int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
# print(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

# dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
# dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

#print(dimX)    # 1280
#print(dimY)    # 720

#print(dimX_cam)    # 1280
#print(dimY_cam)    # 720




#imgY = int(img.shape[0])#/10)
#imgX = int(img.shape[1])#/10)
###################################################
