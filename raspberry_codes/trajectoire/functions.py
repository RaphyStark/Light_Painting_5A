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

