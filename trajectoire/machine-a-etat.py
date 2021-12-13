import cv2 as cv
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.type_check import imag

import AStar


def setup() :
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # print("dimX = {}".format(dimX))
    # print("dimY = {}".format(dimY))

    return cap, dimX, dimY


def read_img():
    success, frame = cap.read()
    if not success :
        print("Can't receive frame (stream end?). Exiting ...")
    return frame


def calc_coord(frame) :

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



# if __name__=='__main__':

# 1. Récupérer la dimension du champ de vision de la caméra
cap, dimX, dimY = setup()


#print(dimX)    # 1280
#print(dimY)    # 720



# nombre de colonnes du tableau img
#dimY = len(img[0])

# nombre de lignes
#dimX = len(img)

#               1ere colonne    2eme colonne ...    1280e colonne
# 1ere ligne    occG[0][0]
# 2eme ligne
# ...
# 720                                               occG[719][1279]

dimX = int(dimX)
dimY = int(dimY)



#print(dimX)    # 1280
#print(dimY)    # 720

# 2. Générer une matrice d'occupation aléatoire
img = cv.imread("out3.jpg")



img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

img = cv.GaussianBlur(img, (5,5), 3, 3)

img = cv.Canny(img,170,200, True)

img = cv.threshold(img, 130, 1, 0)
img = img[1]

#print(img.shape[0])    #890
#print(img.shape[1])    #970

dimY = int(img.shape[0]/10)
dimX = int(img.shape[1]/10)

img = cv.resize(img, (dimX, dimY))




#print(len(img[len(img)-1]))

# quand j'affiche la dernière ligne du tableau
# il m'affiche 128 éléments

wait=[]
list=[]

#print(img[dimY-1][dimX-1])

# on créé une liste de ligne de la grille
for y in range(0, dimX):
    for x in range(0, dimY):
        wait.append(img[x][y])
    list.append(wait)
    wait=[]

list = np.array(list)

#'''
#occupancyGrid = np.zeros([dimX-1, dimY-1])
occupancyGrid = list
# max adjacency degree
adjacency = 8

# create and plot map
carte = AStar.Map(dimX, dimY, adjacency)
carte.initCoordinates()

#carte.generateRandObstacles()

#print("load")
carte.loadOccupancy(occupancyGrid)
#print("genere")
carte.generateGraph()

noFig = 0
#print("plot")
carte.plot(noFig)
plt.show()
#'''

'''
# 3. Récupérer les coordonnées initiales du robot
frame = read_img()
x0, y0 = calc_coord(frame)


# 4. Trouver le noeud correspondant
# TODO : parcourir listOfNodes pour trouver le noeud correspondant
startNodeNo = 0


# 5. Générer aléatoirement les coordonnées du noeud d'arrivée
# TODO
goalNodeNo = 5



# 6. Générer un chemin avec l'algorithme A*
closedList, successFlag = carte.AStarFindPath(startNodeNo,goalNodeNo, epsilon=1.0)
if (successFlag==True):
    path, lenpath = carte.builtPath(closedList)


# 7. Générer une liste de points de passage
WPlist = []
for i in range(len(path)):
    current_node = path[i]
    coord = []
    coord.append(carte.graph.listOfNodes[current_node].x)
    coord.append(carte.graph.listOfNodes[current_node].y)
    WPlist.append(coord)


# boucle de commande du robot

    # créer une meilleure condition pour la loop 
    # while 

    # WP navigation: switching condition to next WP of the list
    if WPManager.distanceToCurrentWP(robot.x, robot.y) <= epsilonWP :
        WPManager.switchToNextWP()

    # calcul de V et Omega en fonction de la position et du next point







# 8. Obtenir les coordonnées du robot grâce au script python de localisation

# while robot.coord.toNodeNo != goalNodeNo





# When everything done, release the capture
cap.release()


'''
