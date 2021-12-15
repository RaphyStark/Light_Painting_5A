import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import cv2 as cv




def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)
    return cap

def setup(img_X, img_Y) :
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    #dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    #dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    print(img_X)
    print(img_Y)

    print(int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

    #if (dimX >= img_X and dimY >= img_Y):
    #cap = change_res(cap, img_X, img_Y)
    cap.set(3, img_X)
    cap.set(4, img_Y)

    print(int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))


    dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    return cap, dimX, dimY


def calc_coord(cap) :
    success, frame = cap.read()
    if not success :
        print("Can't receive frame (stream end?). Exiting ...")
    if not success :
        print("cap read not successed")   
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
            X = int(M["m10"] / M["m00"])    
            Y = int(M["m01"] / M["m00"])
        return X, Y