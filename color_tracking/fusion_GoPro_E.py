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

pixel_list =[]
#Gestion des frames de la vidéo
def gestion_frame():
      
    cap = cv.VideoCapture(0)
    success, frame = cap.read()
    currentframe = 0

    # créer un dossiers pour stocker les frames s'il n'existe pas 
    if not os.path.exists('frames'):
        os.mkdir('frames')
    print(success)
    while success:
    # Capture frame-by-frame
        success, frame = cap.read()
    
    # Quitter s'il n'y a plus de frame dans la vidéo
        if not success:
            break
    
    #cv.imshow("output", frame)
        cv.imwrite('frames/'+str(currentframe)+ '.jpg', frame)  # save frame as JPEG file
        print ("Frame number: ", currentframe)
        calcul_coord(frame)
        print(" ")
      #  if cv.waitKey(10) == 27:
       #     break
        currentframe += 1
   

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
 


def calcul_coord(src):
       
    # convert the image to grayscale
    gray_image = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    gray_image = cv.blur(gray_image, (5,5))
    
 #   canny_output = cv.Canny(gray_image, threshold, threshold * 2)
    # convert the grayscale image to binary image
    ret,thresh = cv.threshold(gray_image,127,255,0)
   
    # find contours in the binary image
    contours, hierarchy= cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)#center
    
 #   contours2, hierarchy2 = cv.findContours(canny_output, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)#contour 
    
   # drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    
    """
    for i in range(len(contours2)):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        cv.drawContours(drawing, contours2, i, color, 2, cv.LINE_8)
    """
    
    for c in contours:
       # calculate moments for each contour
       M = cv.moments(c)
       
        # calculate x,y coordinate of center
       cX = int(M["m10"] / M["m00"])
       cY = int(M["m01"] / M["m00"])
    
     #  cv.circle(src, (cX, cY), 5, (255, 255, 255), -1)
     #  cv.putText(src, "centroid", (cX - 25, cY - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
       # display the image
     #  cv.imshow("Image", src)
        
       pixel_list.clear()
       pixel_list.append([cX,cY])
       
    #Print the coordinates    
    print(pixel_list)

gestion_frame()

