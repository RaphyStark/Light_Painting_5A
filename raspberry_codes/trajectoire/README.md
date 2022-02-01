###### explications sur certaines parties du code ######


# RESIZE LA CAPTURE
# MACBOOK_CAM_ORIGINAL_HEIGHT = 720
# MACBOOK_CAM_ORIGINAL_WIDTH = 1280
# LOGITECH_CAM_ORIGINAL_HEIGHT = 1080
# LOGITECH_CAM_ORIGINAL_WIDTH = 1920
# LOGITECH_RESIZE_HEIGHT    :  90, 288, 480, 600, 896, 1080
# LOGITECH_RESIZE_WIDTH     : 160, 352, 640, 800, 1600, 1920

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