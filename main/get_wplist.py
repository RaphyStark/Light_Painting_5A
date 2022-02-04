#from functions import *
from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt 
import Robot as rob
from functions import map
import numpy as np
import math
import AStar
import os
import cv2 as cv

capX = 352
capY = 288


def set_draw_dimensions(capX, capY):
    # 1. Import image
    img = cv.imread("spirale.jpg")

    # 2. Resize image at capX, capY
    img = cv.resize(img, (capX, capY))

    # 3. Passage en nuances de gris
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 4. Passage en binaire
    img = cv.threshold(img, 200, 1, 0)
    img = img[1]

    # 5. Inversion des obstacles et des cases libres
    print("inverting bits...")
    for i in range(len(img)):
        for j in range (len(img[0])) :
            if img[i][j] == 0:
                img[i][j] = 1
            else :
                img[i][j] = 0 
    return img

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

def WP_generator(carte, path):
    WPlist = []
    for i in range(len(path)):
        current_node = path[i]
        coord = []
        coord.append(carte.graph.listOfNodes[current_node].x)
        coord.append(carte.graph.listOfNodes[current_node].y)
        WPlist.append(coord)
    return WPlist



# resize light painting image dimensions at camera resolution
img = set_draw_dimensions(capX, capY)

# generate map
carte = generate_carte(img, capX, capY)

# get start node from click
node_x, node_y = get_nodes(carte)
start = capX * node_y + node_x
startNode = carte.graph.listOfNodes[start]

# get goal node from click
node_x, node_y = get_nodes(carte)
goal = capX * node_y  + node_x
goalNode = carte.graph.listOfNodes[goal]

# generate path
print("finding the path...")
closedList, successFlag = carte.AStarFindPath(start, goal, epsilon=0.1)
if (successFlag==True):
    print("building the path...")
    path, lenpath = carte.builtPath(closedList)
    print("plotting the path...")
    carte.plotPathOnMap(path, 1)
    plt.show()
else :
    print("error generating waypoint")
    exit()

print("please close this final plot")
plt.close('all')

# generate WPlist
WPlist = WP_generator(carte, path)

print(WPlist)