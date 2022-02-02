#from functions import *
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt 
import Robot as rob
import numpy as np
import math
import AStar
import os
import cv2 as cv

capX = 352
capY = 288
coeff = 1


# PROBLEME
# Si on resize à 160 90 la caméra ne voit pas à plus d'1 mètre
# Resize à plus que 160 90 (200 200 par exemple) peut résoudre le problème
# mais implique un temps de path build plus long
# l'autre solution est de jouer sur les paramètres (blur etc.)


# functions

# main step 1
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
    print("capX before = " + str(capX))
    print("capY before = " + str(capY))

    # 2.1. Set dimensions
    #cap.set(cv.CAP_PROP_FRAME_WIDTH, LOGITECH_RESIZE_WIDTH)
    #cap.set(cv.CAP_PROP_FRAME_HEIGHT, LOGITECH_RESIZE_HEIGHT)

    # 2.2. On récupère les nouvelles valeurs dans capX et capY
    #capX = cap.get(cv.CAP_PROP_FRAME_WIDTH)#160
    #capY = cap.get(cv.CAP_PROP_FRAME_HEIGHT)#90

    """
    print("capX after set = " + str(capX))
    print("capY after set = " + str(capY))
    """
    
    capX = 100
    capY = 100

    """
    # 2.3. On vérifie les valeurs des variables après modification
    print("capX after = " + str(capX))
    print("capY after = " + str(capY))
    """

    # 2.4. On vérifie la possibilité de prendre une capture dans le flux
    success, frame = cap.read()
    if success is True :
        frame = cv.resize(frame, (capX, capY))
        if capX == int(frame.shape[1]) and capY == int(frame.shape[0]) :
            print("OK")
        else:
            print("resizing frame not working")
            exit()

    else :
        print("Problem capturing a frame")
        exit()

    # 2.5 on retourne capX, capY
    return cap, capX, capY

# main step 2
def set_draw_dimensions(capX, capY):
    # 3. Set draw img at VideoCapture new dimensions

    # 3.1. Import image
    img = cv.imread("spirale.jpg")

    # 3.2. Resize image at capX, capY
    img = cv.resize(img, (capX, capY))

    # 4.1. Passage en nuances de gris
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 4.2. Passage en binaire
    img = cv.threshold(img, 200, 1, 0)
    img = img[1]

    # 4.3. Inversion des obstacles et des cases libres
    #def map(x, in_min, in_max, out_min, out_max):
    print("inverting bits...")
    for i in range(len(img)):
        percent_i = map(i, 0, len(img), 0, 100)
        print(str(percent_i) + "%")
        for j in range (len(img[0])) :
            if img[i][j] == 0:
                img[i][j] = 1
            else :
                img[i][j] = 0
            percent_j = map(i, 0, len(img[0]), 0, 100)
            print("colomn " + str(i) + " = " + str(percent_i) + "%")    
            print("line " + str(j) + " = " + str(percent_j) + "%")    
    return img



# main step 3
def generate_carte(img, capX, capY):

    print("loading occupancy grid...")
    # 3.1 Chargement du tableau occupancyGrid
    wait=[]
    list=[]
    for y in range(0, capX):
        for x in range(0, capY):
            wait.append(img[x][y])
        list.append(wait)
        wait=[]
    list = np.array(list)
    occupancyGrid = list

    print("generating graph...")
    # 3.2 Création de la carte (objet Map)
    adjacency = 4
    carte = AStar.Map(capX, capY, adjacency)
    carte.initCoordinates()
    carte.loadOccupancy(occupancyGrid)
    carte.generateGraph()
    
    return carte



# main step 4
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
            print("please close the window")

    ## Affichage de la carte
    fig1 = plt.figure()
    carte.plot(1)
    # Définition d'un objet coordonnées
    coord = Coord()
    # Connection de la souris et du click
    binding_id = plt.connect('motion_notify_event', on_move)
    plt.connect('button_press_event', on_click)
    # attente du click de l'utilisateur
    print("click somewhere in a white box...")
    # Affichage de la carte
    plt.show()
    node_x = round(coord.x)
    node_y = round(coord.y)
    print(node_x)
    print(node_y)
    plt.close()

    return node_x, node_y

"""
# main step 5 : Générer un chemin entre les deux noeuds avec l'algorithme A*
def generate_path(carte, start, goal):
    closedList, successFlag = carte.AStarFindPath(start, goal, epsilon=0.1)
    if (successFlag==True):
        path, lenpath = carte.builtPath(closedList)
        print("path : " + str(path))
        carte.plotPathOnMap(path, 1)
        plt.show()
    else :
        print("error generating waypoint")
        exit()

    print("please close this final plot")
    plt.close('all')
    return path
"""

# main step 6
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




# main step 2 : resize light painting image dimensions
img = set_draw_dimensions(int(capX/coeff), int(capY/coeff))


# main step 3 : generate carte
carte = generate_carte(img, int(capX/coeff), int(capY/coeff))


# POUR SPIRALE.JPG
# start_node :  node_x : 316, node_y = 236  (début spirale)
# goal_node :   node_x : 161, node_y = 161  (fin spirale)

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
print("finding the path")
closedList, successFlag = carte.AStarFindPath(start, goal, epsilon=0.1)
if (successFlag==True):
    print("building the path...")
    path, lenpath = carte.builtPath(closedList)
    #print("path : " + str(path))
    #print("plotting the path...")
    #carte.plotPathOnMap(path, 1)
    plt.show()
else :
    print("error generating waypoint")
    exit()

print("please close this final plot")
plt.close('all')

# main step 6 : generate WPlist
WPlist = WP_generator(carte, path)

print(WPlist)