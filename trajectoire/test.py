import cv2 as cv
import numpy as np

# TEST FILE : GET LUMPOINT COORD

# TODO
# 3. Faire correspondre les dimensions de la carte avec celles de la caméra

# DOING
# convertir coordonnées pixel en noeud (à un facteur d'échelle près)    


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


robotX = 0
robotY = 0
robotX_precedent = 0
robotY_precedent = 0
robotOmega = 0
robotOmega_precedent = 0
robotTheta = 0

OK = True
while OK is True :
    success, frame = cap.read()
    # currentframe = 0
    if not success :
        print("cap read not successed")
        OK = False
        
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q') :
        OK = False

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
            robotX_precedent = robotX
            robotY_precedent = robotY
            robotX = int(M["m10"] / M["m00"])    
            robotY = int(M["m01"] / M["m00"])
            robotOmega_precedent = robotOmega
            robotOmega = np.arctan2(robotY_precedent - robotY, robotX_precedent - robotX)
            robotTheta = robotOmega_precedent + robotOmega


    print("robotX = " + str(robotX))
    print("robotY = " + str(robotY))
    print("robotXprecedent = " + str(robotX_precedent))
    print("robotYprecedent = " + str(robotY_precedent))
    print("robot theta = " + str(robotTheta))

    



# orientation initiale theta = 0
# rotation de 90°
# nouvelle orientation = 90° (0+90)
# rotation de -45°
# nouvelle orientation = 45° (0+90-45)

# COMMENTAIRES

#x0 = carte.graph.listOfNodes[robotNodeNo].x
#y0 = carte.graph.listOfNodes[robotNodeNo].y
#print("x0 = " + str(x0))
#print("y0 = " + str(y0))


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
#################################################