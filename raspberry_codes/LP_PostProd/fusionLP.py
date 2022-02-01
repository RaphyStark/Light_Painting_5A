from PIL import Image
import cv2 as cv
import glob
import os 

def rm_Background(img):
    img = Image.open(img)

    # Conversion 
    img = img.convert("RGBA")
    
    #recherche des pixels à 0
    datas = img.getdata()
    #print(datas)
    
    newData = []

    for item in datas:
        if item[0] <= 200 and item[1] <= 200 and item[2] <=200:
            newData.append((0,0,0,0))
        else:
            newData.append(item)
    print(img)
    img.putdata(newData)
    
    print("successful")
    return img
    
fusion = Image.open("0.jpg")
fusion.save("./fusion.png")
currentFusion = 0

i = 0
while (i < 1312) :
#for i in range (0,1312):
    filename= str(str(i) + ".jpg")
    img =rm_Background(filename)
    
    # Sauvegarde des images 
    fusion.paste(img,(0,0), mask = img)
    fusion.save(str("currentfusion"+str(i)+".png"))
    i = i + 100
    print(i)

fusion.save("./fusion.png")    
fusion.show()

# Vidéo Light Painting
img = cv.imread("currentfusion0.png")
dimX = img.shape[1]
dimY = img.shape[0]
frameSize = (dimX, dimY)

#out = cv.VideoWriter('output_video.avi',cv.VideoWriter_fourcc(*'DIVX'), 60, frameSize)
out = cv.VideoWriter('out.avi', cv.VideoWriter_fourcc(*'DIVX'), 1, frameSize)
   
i = 0
while (i < 1312) :
#for i in range (0,1312):
    filename= str("currentfusion"+str(i)+".png")
    img = cv.imread(filename)
    out.write(img)
    i =i + 100
out.release()
#cv.destroyAllWindows()
