import cv2 as cv
import numpy as np
#import codes/AStar

def setup()
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    success, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # print("dimX = {}".format(dimX))
    # print("dimY = {}".format(dimY))

    return cap, dimX, dimY


def calc_coord()
    if success :
        success, frame = cap.read()

        # convert the image to grayscale
        gray_image = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
        gray_image = cv.blur(gray_image, (5,3))

        ret,thresh = cv.threshold(gray_image,127,255,0)

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


# 2. Générer une matrice d'occupation aléatoire
occupancyGrid = np.zeros([dimX, dimY])
# TODO : générer des obstacles aléatoirement


# 3. Récupérer les coordonnées initiales du robot
robot.x0, robot.y0 = calcul_coord(frame)


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