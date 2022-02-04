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

        $ ssh-keygen -t ed25519 -C "your_email@example.com" \
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