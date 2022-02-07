import cv2 as cv
import numpy as np

def get_coord(cap, capX, capY, robot, current_frame) :
    # get a frame in camera stream
    success, frame = cap.read()
    if not success :
        print("cap read not successed")
        exit()
    
    # image processing
    frame = cv.resize(frame, (capX,capY))
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame = cv.blur(frame, (5,3))
    success, frame = cv.threshold(frame,127,255,0)
    if not success :
        print("threshold not successed")
        exit()

    # get light point coordonates
    contours, hierarchy = cv.findContours(frame, cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)
    for c in contours:
        M = cv.moments(c)
        if (M["m00"] != 0) :
            robotX = int(M["m10"] / M["m00"])
            robot.x = int(robotX)
            robotY = int(M["m01"] / M["m00"])
            robot.y = int(robotY)

    # save frame for post production
    cv.imwrite('frames/'+str(current_frame)+ '.jpg', frame)  # save frame as JPEG file
    current_frame += 1

    # show in a window
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q') :
        exit()


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def debug(robot, WPManager):
    name = "./output.csv"
    XP = "XP = " + str(robot.px)
    YP = "YP = " + str(robot.py)
    XC = "XC = " + str(robot.x)
    YC = "YC = " + str(robot.y)
    XR = "XR = " + str(WPManager.xr)
    YR = "YR = " + str(WPManager.yr)
    THETAC = "thetaC = " + str(robot.theta * 57.295779513)
    THETAR = "thetaR = " + str(robot.theta_ref * 57.295779513)
    WD_REF = "wD_ref = " + str(robot.wD_ref)
    WG_REF = "wG_ref = " + str(robot.wG_ref)
    
    with open(name, "a") as o:    
        print("previous position :")
        print(XP, file = o)
        print(YP, file = o)
        print(XP)
        print(YP)
        print("current position :")
        print(XC, file = o)
        print(YC, file = o)
        print(XC)
        print(YC)
        print("next position")
        print(XR, file = o)
        print(YR, file = o)
        print(XR)
        print(YR)
        print("thetas")
        print(THETAC, file = o)
        print(THETAR, file = o)
        print(THETAC)
        print(THETAR)
        print("tensions")
        print(WD_REF, file = o)
        print(WG_REF, file = o)
        print(WD_REF)
        print(WG_REF)
        print()
        print()
        print()
        o.close()


def debug2(robot, WPManager):
    # calcul des erreurs
    errorV = (np.sqrt((WPManager.xr - robot.x) ** 2 + (WPManager.yr - robot.y) ** 2))
    errorw = (robot.theta_ref - robot.theta)
    print("error speed = " + str(errorV))
    print("error theta = " + str(errorw))
    print()
    print()
    print()