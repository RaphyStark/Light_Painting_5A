
import cv2 as cv


# every loop functions
def get_coord(cap, capX, capY, robot, current_frame) :

    success, frame = cap.read()
    if not success :
        print("cap read not successed")
        exit()

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

    cv.imwrite('frames/'+str(current_frame)+ '.jpg', frame)  # save frame as JPEG file
    current_frame += 1

    #"""
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q') :
        exit()
    #"""
    # step 6 : get lighting point coordinates
    contours, hierarchy = cv.findContours(frame, cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS)
    for c in contours:
        M = cv.moments(c)
        if (M["m00"] != 0) :
            robotX = int(M["m10"] / M["m00"])
            robot.x = int(robotX)
            robotY = int(M["m01"] / M["m00"])
            robot.y = int(robotY)


def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)




def debug(robot, WPManager):
    print("current position :")
    print("XP = " + str(robot.px))
    print("YP = " + str(robot.py))
    print("XC = " + str(robot.x))
    print("YC = " + str(robot.y))
    print("XR = " + str(WPManager.xr))
    print("YR = " + str(WPManager.yr))
    print()
    print("thetaC = " + str(robot.theta * 57.295779513))
    print("thetaR = " + str(robot.theta_ref * 57.295779513))
    print("wD_ref = " + str(robot.wD_ref))
    print("wG_ref = " + str(robot.wG_ref))  
    print()
    print()