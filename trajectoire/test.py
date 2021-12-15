import cv2 as cv


# TODO
# 3. Faire correspondre les dimensions de la carte avec celles de la caméra

# DOING
# convertir coordonnées pixel en noeud (à un facteur d'échelle près)    


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True :
    success, frame = cap.read()
    # currentframe = 0
    if not success :
        print("cap read not successed")
        break
        
    cv.imshow('frame', frame)
    cv.waitKey(20)

    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_image = cv.blur(gray_image, (5,3))
    success,thresh = cv.threshold(gray_image,127,255,0)
    if not success :
        print("threshold not successed")

    robotX = 0
    robotY = 0    

    # find contours in the binary image
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)
    for c in contours:
        # calculate moments for each contour
        M = cv.moments(c)
        # calculate x,y coordinate of center           
        if (M["m00"] != 0) :
            robotX = int(M["m10"] / M["m00"])    
            robotY = int(M["m01"] / M["m00"])

    print("robotX = " + str(robotX))
    print("robotY = " + str(robotY))
