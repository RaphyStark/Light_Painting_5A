Ce README se présente en deux parties: \
- Présentation du projet
- Configuration de la Raspberry Pi

# Light_Painting_5A

Light Painting 5A est un projet faisant suite au projet "Mobile Robot LightPainting". \
Il a pour but de mettre en place un système de contrôle à distance des robots, et d'automatiser les commandes. \
Nous nous affranchissons donc de coder en dur les instructions moteurs en fonction du temps pour la réalisation. \
Ici, la réalisation sera recréée à partir d'une image/dessin de ce que l'on souhaite faire. 

## Hardware

- une Raspberry Pi 3B+ ou 4 
- une Arduino Mega 
- base robotique Romi Chassis Kit de Pololu (réf 3500) + moteurs, encodeurs, roues et Neopixel
- Modules NRF24L01 (1 pour la RPI et 1 pour le robot) 
ATTENTION : Les Arduino disposent d'un régulateur de tension (SPX1117M3-L-5 Regulator) qui se chargent de stabiliser l'alimentation électrique. \
En revanche, si le module est connecté directement à une chip ATmega328, il faut ajouter un condensateur.
- Caméra 

###Branchement
PINTYPE		RPI		ARDUINO		MODULE \

GND		    GND		GND		    1 \
VCC		    1/17	3,3V     2 (3,3V!) \
CE0	     15		 22	     	3 \
CSN	 	   24		 23		     4 \
SLCK/SCK	23	  52     		5	 \
MOSI		   19		 51	     	6 \
MISO		   21		 50     		7 \

## Software
 
- Python + virtualenvs
- git
- VNC (pour travailler sur la RPI en remote sans écran)
- RF24 \
Pour les installations voir le readme: installation

## Le Projet 

Nous utilisons une Raspberry Pi 4 avec un module nRF24 pour la communication radio, une caméra connectée à la RPI qu'il faudra accrocher au plafond, et une carte Arduino
MEGA avec module nRF24 qui sera placé sur le robot. Une Neopixel est connecté à l'Arduino. 

La RPI devra avoir OpenCV d'installé, ainsi que la librairie du nRF24. \
L'arduino devra avoir la librairie nRF24 d'installée aussi. 

Dans le dossier Arduino_codes: \
Se trouve le code pour initialiser la neopixel ainsi que la fonction à appeler pour modifier sa couleur. (neopixel>neopixel.ino) \
Dans le dossier Deplacement se trouve le code permettant de controler les robots. \
Ce code contient les fonctions pour récupérer les valeurs moteurs via le module de communication et les exécuter. \
Il possède aussi les fonctions pour gérer la neopixel.(deplacement.ino) \
Le dossier Deplacement contient aussi les librairies pour l'utilisation des encodeurs, des moteurs, et l'asservissement de ceux-ci via un PID. 

Dans le dossier Raspberry_codes: \
Se trouve un premier dossier, LP_PostProd, permettant de créer, à partir des images récupérées lors d'une réalisation, une vidéo de celle-ci, une vidéo du lightpainting, 
et l'image final du lightpainting. \
Un dossier trajectoire contenant le programme de la RPI. Les codes AStar.py, Timer.py, Robot.py, functions.py sont utilisés dans le main.py. 

Spirale.jpg est notre image de test. C'est une image en blanc sur fond noir créé sous Paint. A partir de cette image nous allons créér une grille d'occupation. \
Une fois un noeud de début et de fin selectionnés, l'algorithme va créer une trajectoire entre ces deux noeuds. \
La grille d'occupation nous permet de faire semblant qu'il y a des obstacles dans notre espace de travail, ainsi forçant l'algorithme de génération de trajectoire à en générer une ayant la forme que l'on souhaite. \
La caméra nous permet d'enregistrer les images de la réalisation. A partir de ces images nous pouvons connaitre la position actuelle du robot. \
En utilisant les positions précédentes nous pouvons déduire l'orientation du robot. Cette méthode perd en précision au fur et à mesure de la réalisation. \
Une amélioration possible du projet est donc d'ajouter une centrale inertielle au robot. 

