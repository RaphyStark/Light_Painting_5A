Ce README se présente en deux parties: 
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

###Branchement \
PINTYPE \t		RPI	\t	ARDUINO	\t	MODULE \

GND		\t    GND	\t	GND		\t    1 \
VCC		\t    1/17	\t 3,3V  \t   2 (3,3V!) \
CE0	 \t    15	\t	 22	   \t  	3 \
CSN	 \t	   24	\t	 23		  \t   4 \
SLCK/SCK \t	23	\t  52   \t  		5	 \
MOSI	\t	   19	\t	 51	   \t  	6 \
MISO	\t	   21	\t	 50    \t 		7 \

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



## Premiere utilisation de la Raspberry Pi
Bien qu'il soit possible d'utiliser la Raspberry Pi avec VNC sans disposer d'écran, sa configuration au premier lancement nécessite de voir ce qui est écrit à l'écran et pour activer ssh et VNC.

Une autre solution (headless) consiste à écrire dans la partition boot du Raspberry pour configurer ssh et lui donner le SSID et Password du réseau local.

Une fois le Raspberry Pi configuré et sur le même réseau que le PC, taper raspberrypi.local dans VNC à l'endroit de l'adresse IP de la nouvelle connexion.


## Environnement virtuel LightPainting
https://opensource.com/article/21/2/python-virtualenvwrapper \
Voir la dernière section de ce fichier pour comprendre l'interet de l'environnement virtuel

    $ sudo pip3 install virtualenvwrapper
    
    $ gedit .bashrc

Ajouter à la fin les lignes suivantes :\
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 \
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv \
source /usr/local/bin/virtualenvwrapper.sh

Création d'un environnement virtuel (attention à ne pas de ajouter de "-" cf.setup.py de RF24)

    $ mkvirtualenv LightPainting --always-copy
    
L'option --always-copy assure (à vérifier) que le virtualenv créer bien les lib dans le virtualenv

    $ cd LightPainting
    

## Branchements du RF24
http://electroniqueamateur.blogspot.com/2017/02/communication-entre-raspberry-pi-et.html


## Installation de RF24 depuis les sources sur la RaspberryPi
https://github.com/nRF24/RF24/issues/615 

    $ mkdir rf24libs

    $ cd rf24libs

    $ git clone https://github.com/TMRh20/RF24

    $ cd RF24

    $ ./configure --prefix=/home/pi/.virtualenvs/LightPainting/bin

L'option --prefix permet d'indiquer à ./configure où installer la lib \
On remarquera plus loin à la fin de la commande sudo python3 setup.py install : \
librf24.so found at /home/pi/.virtualenvs/LightPainting/bin/lib \
Et à la fin de la commande sudo make install : \
Installing Libs to /home/pi/.virtualenvs/light-painting/bin/lib

    $ sudo make install

    $ sudo apt-get install python3-dev libboost-python-dev

    $ sudo ln -s $(ls /usr/lib/arm-linux-gnueabihf/libboost_python39.so | tail -1) /usr/lib/arm-linux-gnueabihf/libboost_python3.so

    $ sudo apt-get install python3-setuptools

    $ cd pyRF24/

    $ /home/pi/.virtualenvs/LightPainting/bin/python3.9 setup.py build

    $ sudo /home/pi/.virtualenvs/LightPainting/bin/python3.9 setup.py install

    $ sudo apt-get install python3-dev python3-rpi.gpio


## Installation de OpenCV sur la Raspberry Pi (toujours dans l'environnement virtuel)

    $ pip3 install opencv-python -v

L'option -v permet de voir où en est l'installation qui peut être assez longue


## Clone du repo Light_Painting_5A avec Git

Utiliser une clé ssh pour récupérer le repo sur son linux :

        $ ssh-keygen -t ed25519 -C "your_email@example.com" \
        > "Enter a file in which to save the key" \
        Cliquer sur entrer \
        Il vous est ensuite demandé de créer un mot de passe pour la clé, entrer une clé \
        $ eval "$(ssh-agent -s)" \
        A ce stade, la commande ci-dessus doit retourner : \
        > Agent pid 59566 (ou un autre nombre) \
        $ open ~/.ssh/config \
        Si la commande ci-dessus retourne : \
        > The file /Users/you/.ssh/config does not exist.
        Il faut créer le fichier ($ touch ~/.ssh/config)
        Sinon modifier le simplement \
        Il faut écrire dans ce fichier : \
        Host * \
          AddKeysToAgent yes \
          IdentityFile ~/.ssh/id_ed25519 \
        Attention, le tuto sur github demande d'ajouter UseKeychain yes, mais ça ne fonctionne pas (sur une RPI3B+) \
        Taper ensuite la commande suivante : \
        $ ssh-add ~/.ssh/id_ed25519 \
        Attention, le tuto sur github demande d'écrire $ ssh-add -K ~/.ssh/id_ed25519 mais ça ne fonctionne pas non plus \
        Il faut à présent se rendre sur les paramètres de son compte github (pas les paramètres du repo \
        Cliquer sur SSH and GPG keys \
        Ajouter tout le contenu de la clé publique SSH créée précédemment (tout ce qui se trouve dans $ cat ~/.ssh/id_ed25519.pub) \
        Enfin, cloner le repo dans le repertoire de son choix : \
        $ sudo apt install git \
        $ git clone git@github.com:RaphyStark/Light_Painting_5A.git



## Instructions utiles concernant l'utilisation de Git

### Envoyer un gros fichier sur git
  https://git-lfs.github.com/

### Créer et push un fichier
        $ git add README.md
        $ git commit -m 'modification README.md'
        $ git push

### Récupérer un dossier du master vers une branch
        $ git checkout <branch_name>
        $ git stash (si besoin)
        $ git checkout <branch_name>
        $ git merge origin/master
        $ git add README.md 
        $ git commit -m 'modif README.md'
        $ git push
        $ git merge origin/master
        $ git fetch
        $ git push
        $ git pull (résoudre les problèmes dans la fenêtre vsc (accept upcoming changes)
        $ git add README.md
        $ git commit -m 'update after merge'
        
        
## Pourquoi installer un environnement virtuel ?
Travailler en python peut sembler difficile : versions 2 et 3 installés sur son PC, différents repertoires d'installations ($ whereis python)...

Il n'est pas recommandé d'utiliser directement l'installation python du système pour travailler.
De plus, on peut s'y perdre facilement (plusieurs repertoires d'installations, Python, Python3...)

Cela peut poser des problèmes lorsqu'on souhaite développer deux applications avec des versions de modules différents.

Il faut donc mettre en place un environnement virtuel dans son worksplace et y installer les modules nécessaires au projet.

cf. https://stackoverflow.com/questions/41992104/usr-bin-python-vs-usr-local-bin-python :
“If it's a virtualenv, that also makes cleanup easier; just delete the virtualenv when you no longer need it as opposed to trying to uninstall libraries installed at the system level.”

Il est également recommandé d'utiliser un environnement virtuel lorsque l'utilisation de certains modules nécessitent une élevation de droits :
https://askubuntu.com/questions/1268870/python-module-not-found-in-sudo-mode-ubuntu-20-04
