import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from functions import *
import AStar






# VARIABLES GLOABLES

LOGITECH_RESIZE_HEIGHT = 90
LOGITECH_RESIZE_WIDTH = 160

MACBOOK_CAM_RESIZE_HEIGHT = 288
MACBOOK_CAM_RESIZE_WIDTH = 352


name = "spirale.jpg"


# 1. Get VideoCapture dimensions
capX = 0
capY = 0

cap = cv.VideoCapture(0)


if not cap.isOpened():
    print("Cannot open camera")
    exit()


capX = cap.get(cv.CAP_PROP_FRAME_WIDTH)
capY = cap.get(cv.CAP_PROP_FRAME_HEIGHT)


# 2. Set VideoCapture dimensions to (capX = 160, capY = 90)
print("capX = " + str(capX))
print("capY = " + str(capY))

cap.set(cv.CAP_PROP_FRAME_WIDTH, LOGITECH_RESIZE_WIDTH)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, LOGITECH_RESIZE_HEIGHT)

capX = cap.get(cv.CAP_PROP_FRAME_WIDTH)	#160
capY = cap.get(cv.CAP_PROP_FRAME_HEIGHT) #90

print("capX = " + str(capX))
print("capY = " + str(capY))

success, frame = cap.read()

if success is True :
    capY = int(frame.shape[0])
    capX = int(frame.shape[1])
else :
    print("Problem capturing a frame")
    exit()


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


# 3. Set draw img at VideoCapture new dimensions
# 3.1. Import image
img = cv.imread(name)
# 3.2. Resize image at VideoCapture dimensions / 10
capX = round(capX/10)
capY = round(capY/10)
print("capX = " + str(capX))
print("capY = " + str(capY))
img = cv.resize(img, (capX, capY))
print("img dim X = " + str(img.shape[1]))
print("img dim Y = " + str(img.shape[0]))





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




###################################################
