### Light_Painting_5A

Light Painting 5A est un projet faisant suite au projet "Mobile Robot LightPainting". 
Il a pour but de mettre en place un système de contrôle à distance des robots, et d'automatiser les commandes. 
Nous nous affranchissons donc de coder en dur les instructions moteurs en fonction du temps pour la réalisation. 
Ici, la réalisation sera recréée à partir d'une image/dessin de ce que l'on souhaite faire. 

Nous utilisons une Raspberry Pi 4 avec un module nRF24 pour la communication radio, une caméra connectée à la RPI qu'il faudra accrocher au plafond, et une carte Arduino
MEGA avec module nRF24 qui sera placé sur le robot. Une Neopixel est connecté à l'Arduino.

La RPI devra avoir OpenCV d'installé, ainsi que la librairie du nRF24.
L'arduino devra avoir la librairie nRF24 d'installée aussi.

Dans le dossier Arduino_codes:
Se trouve le code pour initialiser la neopixel ainsi que la fonction à appeler pour modifier sa couleur. (neopixel>neopixel.ino)
Dans le dossier Deplacement se trouve le code permettant de controler les robots. 
Ce code contient les fonctions pour récupérer les valeurs moteurs via le module de communication et les exécuter. Il possède aussi les fonctions pour gérer la neopixel.
(deplacement.ino)
Le dossier Deplacement contient aussi les librairies pour l'utilisation des encodeurs, des moteurs, et l'asservissement de ceux-ci via un PID.

Dans le dossier Raspberry_codes:
Se trouve un premier dossier, LP_PostProd, permettant de créer, à partir des images récupérées lors d'une réalisation, une vidéo de celle-ci, une vidéo du lightpainting, 
et l'image final du lightpainting.
Un dossier trajectoire contenant le programme de la RPI. Les codes AStar.py, Timer.py, Robot.py, functions.py sont utilisés dans le main.py. 

Spirale.jpg est notre image de test. C'est une image en blanc sur fond noir créé sous Paint. A partir de cette image nous allons créér une grille d'occupation. Une fois un noeud de début et de fin selectionnés, l'algorithme 
va créer une trajectoire entre ces deux noeuds. La grille d'occupation nous permet de faire semblant qu'il y a des obstacles dans notre espace de travail, ainsi forçant
l'algorithme de génération de trajectoire à en générer une ayant la forme que l'on souhaite. 
La caméra nous permet d'enregistrer les images de la réalisation. A partir de ces images nous pouvons connaitre la position actuelle du robot. En utilisant les positions
précédentes nous pouvons déduire l'orientation du robot. Cette méthode perd en précision au fur et à mesure de la réalisation. Une amélioration possible du projet est 
donc d'ajouter une centrale inertielle au robot.

