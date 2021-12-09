# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 10:41:31 2021

@author: Falitiana
"""

from __future__ import print_function
import cv2 as cv
import random as rng
import os
rng.seed(12345)


def calcul_coord(src):
       
    # convert the image to grayscale
    gray_image = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    gray_image = cv.blur(gray_image, (5,3))


    ret,thresh = cv.threshold(gray_image,127,255,0)

    # find contours in the binary image
    contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_TC89_KCOS) #cv.CHAIN_APPROX_SIMPLE

    # print(contours)

    cX = 0
    cY = 0

    for c in contours:
        # calculate moments for each contour
        M = cv.moments(c)
        # calculate x,y coordinate of center
        #cX += M[0][0]
        #cY += M[0][1]
        
        #cX = int(cX/len(contours))
        #cY = int(cY/len(contours))  

        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        
        # pixel_list.clear()
        pixel_coord.clear() 
        pixel_coord.append([cX,cY])
        
    #Print the coordinates    
    print(pixel_coord)
    print(" ")



# main

pixel_coord =[]

#Gestion des frames de la vidéo    
#cap = cv.VideoCapture('E.mp4')
cap = cv.VideoCapture(0)

success, frame = cap.read()

currentframe = 0

# créer un dossiers pour stocker les frames s'il n'existe pas 
if not os.path.exists('frames'):
    os.mkdir('frames')
print(success)

for i in range(0,1000000):
    break

while success:
    # Capture frame-by-frame
    success, frame = cap.read()

    # Quitter s'il n'y a plus de frame dans la vidéo
    if not success:
        break

    # Sinon écrire l'image en mémoire
    #cv.imshow("output", frame)
    cv.imwrite('frames/'+str(currentframe)+ '.jpg', frame)  # save frame as JPEG file

    # calcul des coordonnées
    calcul_coord(frame)

    currentframe += 1

    print ("Frame number: ", currentframe)
    


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
