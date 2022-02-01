# library imports
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import AStar
from matplotlib.backend_bases import MouseButton 



LOGITECH_RESIZE_HEIGHT = 288
LOGITECH_RESIZE_WIDTH = 352
MACBOOK_CAM_RESIZE_HEIGHT = 288
MACBOOK_CAM_RESIZE_WIDTH = 352


def get_coord(cap, capX, capY) :
    # step 1 : read a frame
    success, frame = cap.read()
    if not success :
        print("cap read not successed")
    # step 2 : resize the frame
    frame = cv.resize(frame, (capX,capY))
    # step 3 : cvtColor
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # step 4 : blur
    frame = cv.blur(frame, (5,3))
    # step 5 : turn into binary frame
    success, frame = cv.threshold(frame,127,255,0)
    if not success :
        print("threshold not successed")
        exit()
    """
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q') :
        exit()
    """
    # step 6 : get lighting point coordinates
    contours, hierarchy = cv.findContours(frame, cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)
    for c in contours:
        M = cv.moments(c)
        if (M["m00"] != 0) :
            robotX = int(M["m10"] / M["m00"])
            robotX = int(robotX)
            robotY = int(M["m01"] / M["m00"])
            robotY = int(robotY)
            return robotX, robotY
        else :
            get_coord(cap, capX, capY)

def get_cam_dimensions() :

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
        #print("capX orginal frame = " + str(capX))
        #print("capY orignal frame = " + str(capY))
    else :
        print("Problem capturing a frame")
        exit()

    # 2.5 on retourne capX, capY
    return cap, capX, capY

def set_draw_dimensions():
    # 3. Set draw img at VideoCapture new dimensions

    # 3.1. Import image
    img = cv.imread("spirale.jpg")

    # 3.2. Resize image at VideoCapture dimensions / 10
    capX = round(capX/10)
    capY = round(capY/10)
    img = cv.resize(img, (capX, capY))


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
    
    return


def generate_carte():

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
    
    return carte



def get_nodes(carte):

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
            print("on_click")


    ## Affichage de la carte
    fig1 = plt.figure()
    carte.plot(1)
    # Connection de la souris et du click
    binding_id = plt.connect('motion_notify_event', on_move)
    plt.connect('button_press_event', on_click)
    
    # Définition d'un objet coordonnées
    coord = Coord()


    # Affichage de la carte
    print("hello 1")
    plt.show()
    
    
    start_node_x = round(coord.x)
    start_node_y = round(coord.y)

    plt.close('all')

    ##
    fig1 = plt.figure()
    carte.plot(1)
    coord = Coord()
    print("hello 2")
    binding_id = plt.connect('motion_notify_event', on_move)
    plt.connect('button_press_event', on_click)
    plt.show()
    goal_node_x = round(coord.x)
    goal_node_y = round(coord.y)
    # doesn't close here
    print("hello 3")


    # 6. Générer les numéros des noeuds de départ et d'arrivée

    # 6.1. Noeud de départ :
    start_node_no   = (capX * start_node_y)  + start_node_x
    #startNode = carte.graph.listOfNodes[start_node_no]

    # 6.2. Noeud d'arrivée :
    goal_node_no    = (capX * goal_node_y)  + goal_node_x
    #goalNode = carte.graph.listOfNodes[goal_node_no]

    # 6.3. Affichage des noeuds
    #print("start node = " + str(startNode))
    #print("goal node = " + str(goalNode))

    return carte, start_node_no, goal_node_no



def generate_path(carte, start_node_no, goal_node_no):
    # 7. Générer un chemin entre les deux noeuds avec l'algorithme A*
    closedList, successFlag = carte.AStarFindPath(start_node_no, goal_node_no, epsilon=0.1)
    if (successFlag==True):
        path, lenpath = carte.builtPath(closedList)
        #carte.plotPathOnMap(path, 1)
        #plt.show()
    else :
        print("error generating waypoint")
        exit()
    return path

def WP_generator(carte, path):
    # 8. Générer une liste de coordonnées de points de passage
    WPlist = []
    for i in range(len(path)):
        current_node = path[i]
        coord = []
        coord.append(carte.graph.listOfNodes[current_node].x)
        coord.append(carte.graph.listOfNodes[current_node].y)
        WPlist.append(coord)
    return WPlist