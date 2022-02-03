

import math
import pygame
from numpy import arctan2


delta = arctan2(2,2)
print(delta)

theta = math.atan2(2, 2)

print(theta)

x0 = 2
y0 = 2

x1 = 4
y1 = 4

x2 = 6
y2 = 6

v1 = pygame.math.Vector2(x1-x0, y1-y0)
v2 = pygame.math.Vector2(x2-x0, y2-y0)
angle = v1.angle_to(v2)


print(angle)