# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:28:06 2021

@author: Falitiana
"""

from __future__ import print_function

import cv2 as cv

import numpy as np

import argparse

import random as rng

rng.seed(12345)



def thresh_callback(val):

    threshold = val



# convert the image to grayscale

    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# convert the grayscale image to binary image

    ret,thresh = cv.threshold(gray_image,127,255,0)


# find contours in the binary image

    im2, contours, hierarchy = cv.findContours(threshold,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    for c in contours:

   # calculate moments for each contour

       M = cv.moments(c)

   # calculate x,y coordinate of center

       cX = int(M["m10"] / M["m00"])

       cY = int(M["m01"] / M["m00"])

       cv.circle(img, (cX, cY), 5, (255, 255, 255), -1)

       cv.putText(img, "centroid", (cX - 25, cY - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
       
   # display the image
       cv.imshow("Image", img)
       cv.waitKey(0)

    


# Load source image

parser = argparse.ArgumentParser(description='Code for Finding contours in your image tutorial.')
    
parser.add_argument('--input', help='Path to input image.', default='mandala.jpg')

args = parser.parse_args()
src = cv.imread(cv.samples.findFile(args.input))

if src is None:

    print('Could not open or find the image:', args.input)

    exit(0)

# Convert image to gray and blur it

img = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
img = cv.blur(img, (3,3))


# Create Window

source_window = 'Source'

cv.namedWindow(source_window)
cv.imshow(source_window, src)
max_thresh = 255
thresh = 100 # initial threshold
cv.createTrackbar('Canny Thresh:', source_window, thresh, max_thresh, thresh_callback)
thresh_callback(thresh)
cv.waitKey()