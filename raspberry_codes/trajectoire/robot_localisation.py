import cv2 as cv


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