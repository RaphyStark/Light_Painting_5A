from functions import *
import Robot as rob
import numpy as np
import math
import os


capX = 352
capY = 288
coeff = 1





# main step 2 : resize light painting image dimensions
img = set_draw_dimensions(int(capX/coeff), int(capY/coeff))


# main step 3 : generate carte
carte = generate_carte(img, int(capX/coeff), int(capY/coeff))


# POUR SPIRALE.JPG
# start_node :  node_x : 316, node_y = 236  (début spirale)
# goal_node :   node_x : 161, node_y = 161  (fin spirale)

# main step 4.A : get start node from click
node_x, node_y = get_nodes(carte)
start = (int(capX/coeff) * node_y)  + node_x
startNode = carte.graph.listOfNodes[start]


# main step 4.B : get goal node from click
node_x, node_y = get_nodes(carte)
goal = (int(capX/coeff) * node_y)  + node_x
goalNode = carte.graph.listOfNodes[goal]


# main step 5 : generate path
#path = generate_path(carte, start, goal)
print("finding the path")
closedList, successFlag = carte.AStarFindPath(start, goal, epsilon=0.1)
if (successFlag==True):
    print("building the path...")
    path, lenpath = carte.builtPath(closedList)
    #print("path : " + str(path))
    #print("plotting the path...")
    #carte.plotPathOnMap(path, 1)
    plt.show()
else :
    print("error generating waypoint")
    exit()

print("please close this final plot")
plt.close('all')

# main step 6 : generate WPlist
WPlist = WP_generator(carte, path)

print(WPlist)