# library imports
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import AStar
from matplotlib.backend_bases import MouseButton 



def generate_carte():
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