"""
this script takes a video, 
split it in frames in a directory
and finally takes all the frames and put them into a video again

there is also a function to calculate 
the coord. of a lighting point in a frame

It's usefull when any 
wants to convert a video into frames,
frames into video,
get the coord. of a lighting point in frames and in a video
.......
"""

from __future__ import print_function
import cv2 as cv
import numpy as np
import random as rng
import os
import glob



def calcul_coord(src):
       
    # convert the image to grayscale
    gray_image = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    gray_image = cv.blur(gray_image, (5,3))


    ret,thresh = cv.threshold(gray_image,127,255,0)

    # find contours in the binary image
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS) #cv.CHAIN_APPROX_SIMPLE

    # print(contours)

    for c in contours:
        # calculate moments for each contour
        M = cv.moments(c)

        # calculate x,y coordinate of center        
        if (M["m00"] != 0) :
            cX = int(M["m10"] / M["m00"])    
            cY = int(M["m01"] / M["m00"])
            pixel_coord.clear() 
            pixel_coord.append([cX,cY])
        
    # Print the coordinates    
    # print(pixel_coord)
    # print(" ")

    # Return the coordinates


if __name__=='__main__':
    pixel_coord =[]

    cap = cv.VideoCapture("../E.mp4")
    if not cap.isOpened():
        print("Cannot open file")
        exit()
    success, frame = cap.read()

    currentframe = 0

    # créer un dossiers pour stocker les frames s'il n'existe pas 
    if not os.path.exists('frames'):
        os.mkdir('frames')

    dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    frameSize = (dimX, dimY)    

    while (success and currentframe != 120) :

        # Quitter s'il n'y a plus de frame dans la vidéo
        if not success:
            break

        # Sinon écrire l'image en mémoire
        cv.imwrite('frames/'+str(currentframe)+ '.jpg', frame)  # save frame as JPEG file

        # calcul des coordonnées
        #calcul_coord(frame)

        currentframe += 1

        print ("Frame number: ", currentframe)


        # Capture frame-by-frame
        success, frame = cap.read()

    # When everything done, release the capture
    cap.release()

    #out = cv.VideoWriter('output_video.avi',cv.VideoWriter_fourcc(*'DIVX'), 60, frameSize)
    out = cv.VideoWriter('out.avi', cv.VideoWriter_fourcc(*'DIVX'), 60, frameSize)
    
    for filename in glob.glob('frames/*.jpg'):
        img = cv.imread(filename)
        out.write(img)

    out.release()

    cv.destroyAllWindows()
