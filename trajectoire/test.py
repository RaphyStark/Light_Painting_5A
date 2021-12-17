import cv2 as cv
import numpy as np
import math

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
ProbotX = 0
ProbotY = 0
robotOmega = 0
robotOmega_precedent = 0
robotTheta = 0
mesure = 0


OK = True
while OK is True :
    success, frame = cap.read()

    # currentframe = 0
    if not success :
        print("cap read not successed")
        OK = False
        exit()

    #capX = int(cv.CAP_PROP_FRAME_WIDTH/10)
    #capY = int(cv.CAP_PROP_FRAME_HEIGHT/10)

    # 640
    # 480
    
    capX = 300
    capY = 300

    frame = cv.resize(frame, (capX,capY))#, fx=0.15625, fy=0.20833)
    #print("frame X = " + str(frame.shape[1]))
    #print("frame Y = " + str(frame.shape[0]))




    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_image = cv.blur(gray_image, (5,3))
    success,thresh = cv.threshold(gray_image,127,255,0)

    if not success :
        print("threshold not successed")
        exit()

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q') :
        OK = False

    #X_objectif = round(capX / 2)
    #Y_objectif = round(capY / 2)
    #theta_objectif = 0

    #'''
    # find contours in the binary image
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)
    for c in contours:
        # calculate moments for each contour
        M = cv.moments(c)
        # calculate x,y coordinate of center

        if (M["m00"] != 0) :
            mesure = mesure + 1
            ProbotX = robotX
            ProbotY = robotY
            robotX = int(M["m10"] / M["m00"])    
            robotY = int(M["m01"] / M["m00"])
            
            #robotOmega_precedent = robotOmega_precedent + robotOmega
            ProbotTheta = robotTheta
            #if (robotX)
            robotTheta = np.arctan2(robotY - ProbotY, robotX - ProbotX) # [-Pi, Pi]
            robotTheta = (robotTheta * 180 / np.pi)                     # [-180, 180]
            #if math.fabs(ProbotTheta - robotTheta) > math.pi:
                
            #theta_objectif = np.arctan2(Y_objectif - robotY, X_objectif - robotX) 
            
            #robotTheta = robotOmega_precedent + robotOmega
            
            # passage en degré
             # % 360
            
            print("#### MESURE " + str(mesure) + " ###")
            print("ProbotX = " + str(ProbotX))
            print("ProbotY = " + str(ProbotY))
            print("robotX = " + str(robotX))
            print("robotY = " + str(robotY))
            print("robot theta = " + str(robotTheta))
            print()
            print()

    #'''





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
