###### explications sur certaines parties du code ######


# RESIZE LA CAPTURE
# MACBOOK_CAM_ORIGINAL_HEIGHT = 720
# MACBOOK_CAM_ORIGINAL_WIDTH = 1280
# LOGITECH_CAM_ORIGINAL_HEIGHT = 1080
# LOGITECH_CAM_ORIGINAL_WIDTH = 1920
# LOGITECH_RESIZE_HEIGHT    :  90, 288, 480, 600, 896, 1080
# LOGITECH_RESIZE_WIDTH     : 160, 352,  640, 800, 1600, 1920

# 20, 36 => 240, 432
# 15, 20 => 160, 120



# QUEL PARAMETRE CORRESPOND A QUOI
# frame.shape[0] # => HEIGHT
# frame.shape[1] # => WIDTH

# CALCULER LE NUM D'UN NOEUD SELON DES COORDONNEES
# dimX = 27
# dimY = 25
# size = dimX*dimY
# lastNodeNo = size - 1
# anyNodeNo = (dimX * anyNode.y)  + anyNode.x

# COMMENT JOUER AVEC EPSILON DANS A*
# eps = 1 : A* calssique
# eps = 0 : dijskra
# eps compris entre 0 et 1 : A* pondéré en proba
# eps > 1 : chemin de plus en plus court




# UTILES ?
#import Robot as rob
#import Timer as tmr
#import matplotlib.patches as patches
#from numpy.lib.type_check import imag
#import math





# COMMENTAIRES

#x0 = carte.graph.listOfNodes[robotNodeNo].x
#y0 = carte.graph.listOfNodes[robotNodeNo].y
#print("x0 = " + str(x0))
#print("y0 = " + str(y0))


### COMMENTAIRES UTILES OU OBSOLETES ###



# nombre de colonnes du tableau img
#dimY = len(img[0])

# nombre de lignes
#dimX = len(img)

#               1ere colonne    2eme colonne ...    1280e colonne
# 1ere ligne    occG[0][0] =                            1279
# 2eme ligne                                            
# ...                                                   
# 720                                               occG[719][1279] = 

#dimX = int(dimX)
#dimY = int(dimY)

#print(dimX)    # 1280
#print(dimY)    # 720

#print(img.shape[0])    #890
#print(img.shape[1])    #970

#print(len(img[len(img)-1]))
#print(img[dimY-1][dimX-1])

# img = cv.GaussianBlur(img, (5,5), 3, 3)
# img = cv.Canny(img,170,200, True)

#xf = 12.0
#yf = 12.0
#print("WPManager.xf = " + str(WPManager.xf))
#print("WPManager.yf = " + str(WPManager.yf))

# print("dimX = {}".format(dimX))
# print("dimY = {}".format(dimY))

# print(int(cap.get(cv.CAP_PROP_FRAME_WIDTH)))
# print(int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)))

# dimX = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
# dimY = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

#print(dimX)    # 1280
#print(dimY)    # 720

#print(dimX_cam)    # 1280
#print(dimY_cam)    # 720




#imgY = int(img.shape[0])#/10)
#imgX = int(img.shape[1])#/10)




'''
def find_no_from_coord(dimX, dimY) :
current_node = 0
last_node = dimX*dimY - 1

while (current_node != last_node) :
if carte.graph.listOfNodes[current_node].x == start_node_x :
#print("x ok")

#print(current_node)
if carte.graph.listOfNodes[current_node].y == start_node_y :
#print("y ok")
start_node = current_node
break
else : 
current_node = current_node + 1
else : 
#print(current_node)
current_node = current_node + 1

#print("start node x = " +str(carte.graph.listOfNodes[start_node].x))
#print("start node y = " +str(carte.graph.listOfNodes[start_node].y))


return current_node
'''
#################################################
