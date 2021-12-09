# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 17:02:18 2021

@author: Falitiana
"""

import cv2 as cv
import os

currentframe = 0

cap = cv.VideoCapture('C:/Users/Falitiana/Documents/Python Scripts/E.mp4')
success, frame = cap.read()

if not os.path.exists('C:/Users/Falitiana/Documents/Python Scripts/frames'):
    os.mkdir('C:/Users/Falitiana/Documents/Python Scripts/frames')
    
print(success)    
while success:

    # Capture frame-by-frame
    success, frame = cap.read()
    
    if not success:
        break
    
    #cv.imshow("output", frame)
    cv.imwrite('C:/Users/Falitiana/Documents/Python Scripts/frames/'+str(currentframe)+ '.jpg', frame)  # save frame as JPEG file
    
    
    if cv.waitKey(10) == 27:
        break
    currentframe += 1
   
"""
    # When everything done, release the capture
cap.release()
cv.destroyAllWindows()
"""