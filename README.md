## Environnement Arduino avec NRF24L01


1/ Installer Arduino IDE sur Ubuntu

        $ sudo snap install arduino
        $ sudo usermod -a -G dialout $USER

2/ Installer Arduino IDE sur Windows
        https://www.arduino.cc/en/software

Dans l'onglet outils de Arduino IDE :
Port série :    /dev/ttyACM1 sur Ubuntu COM0 sur Windows
Type de carte : Arduino Mega 2560
Programmateur : AVRISP null

3/ Installer la librairie nécessaire depuis l'onglet Croquis :
Cliquer sur "Importer bibliothèque", "Ajouter librairie".
Taper nrf24L01 dans le champ de recherche et sélectionner RF24.

## Environnement RaspberryPi avec NRF24L01


Connexion à la RPI


Tout d'abord pour accéder au RPI sans écran il faut mettre en place VNCViewer.

Il faut au moins une première fois le brancher à un écran.

Le relier à un réseau WiFi.

Taper ifconfig pour récupérer son ip;

Entrer son ip dans la barre de recherche de VNC.


Il est aussi possible d'écrire dans les fichiers de configuration du boot de la carte SD pour l'obliger à se connecter à un réseau WiFi.

Avec un ordinateur connecté au même réseau que la Raspberry Pi, taper raspberrypi.local dans VNC.


Dans les deux cas, le nom d'utilisateur est pi et le mot de passe raspberry.

Changer par la suite si besoin d'une meilleure sécurité.





https://forums.framboise314.fr/viewtopic.php?f=44&t=1284

Ce tutoriel ne fonctionne pas :
D'abord la librairie libjson0-dev n'existe plus.
Et lorsqu'on la remplace par libjson11-1 (ou encore libjson11-1-dev), on obtient une nouvelle erreur lors de l'execution de la commande make.
Pour corriger cette dernière erreur, il faut changer l'import dans le fichier sender.cpp que le tutoriel demande de télécharger.
L'erreur relative à l'import du json disparait mais de nouvelles aparaissent.
Il semblerait donc que ce tutoriel a été mis en place avec une version trop ancienne de json et qu'il serait alors plus utilisable.

https://forum.raspberry-pi.fr/t/resolu-raspberry-plus-nrf24l01/11219

Ce topic soulève justement le fait que la librairie n'existe plus


https://forum.arduino.cc/t/simple-nrf24l01-2-4ghz-transceiver-demo/405123

Ce lien ne permet que de faire communiquer deux Arduino ensemble.
Il fournit néanmoins les schémas des branchements des modules.
Ainsi que les informations suivantes :
- il est important d'utiliser une capa lorsqu'on utilise la puce Atmega328 sur une breadboard.
Etant donné que la puce est sur une carte Arduino cela n'est pas obligatoire pour le bon fonctionnement du module (même sur une UNO).
- ainsi que des informations techniques sur les modules
Both TX and RX must use the same channel. The default channel for the RF24 library is 76.
When the TX sends a message every RX listening on the same channel will receive the message. The TX includes an “address” in the message and the RX will ignore messages that do not have its address. The address is similar in concept to a phone number except that you cannot easily change the number of your phone. The address is a 5 byte number.


https://forum.arduino.cc/t/communication-sans-fil-arduino-raspberry/197354/3
Cette page ne fournie pas beaucoup d'informations si ce n'est qu'il est possible de retranscrire un code pour Arduino en un code pour RPi à l'aide de wiringpi par exemple, en utilisant les ports GPIO et I2C.

Les réponses fournies à la question posée redirigent vers plusieurs sites internets, notamment :
https://www.carnetdumaker.net/articles/communiquer-sans-fil-avec-un-module-nrf24l01-la-bibliotheque-mirf-et-une-carte-arduino-genuino/
Ce site utilise la bibliothèque mirf, qui permet une communication bidirectionnelle.
Ainsi que ce site:
https://www.carnetdumaker.net/articles/communiquer-sans-fil-en-433mhz-avec-la-bibliotheque-virtualwire-et-une-carte-arduino-genuino/
Qui utilise la bibliothèque virtualwire.


https://lastminuteengineers.com/nrf24l01-arduino-wireless-communication/

Cette page explique le fonctionnement du module nrf24l01.

Il compare également les deux versions de module nrf24l01 :
- nrf24l01 + wireless module (la version compacte que nous avons avec une antenne intégrée)
- nrf24l01 + PA/LNA module (version avec antenne externe et une chip pour gérer le PA/LNA & transmission-reception)
La différence est que cette dernière version permet une transmission sur 1000m (pas utile pour notre projet).

Il explique également comment se fait la transaction avec accusé de reception et interruption (IRQ) :
Transaction with acknowledgement and interrupt :
The transmitter starts a communication by sending a data packet to the receiver. 
Once the whole packet is transmitted, it waits (around 130 µs) for the acknowledgement packet (ACK packet) to receive. 
When the receiver receives the packet, it sends ACK packet to the transmitter. 
On receiving the ACK packet the transmitter asserts interrupt (IRQ) signal to indicate the new data is available.

Il y a également un paragraphe pour les branchements :
CTRL-F : "Wiring – Connecting nRF24L01+ transceiver module to Arduino UNO"

Ainsi qu'un autre paragraphe pour la mise en place de l'environnement :
CTRL-F : "RF24 Arduino Library for nRF24L01+ Module"

Enfin, il fournit les codes pour la communication entre deux Arduinos (un transmitter et un receiver)
CTRL-F : "Arduino Code – For Transmitter"
CTRL-F : "Arduino Code – For Receiver"

La dernière partie du tutoriel fournit des indications pour améliorer le dispositif si des problèmes survenaient.


https://tlfong01.blog/2020/01/24/raspberry-pi-3-tutorial-14-wireless-pi-to-arduino-communication-with-nrf24l01/



https://nrf24.github.io/RF24/md_docs_linux_install.html


http://electroniqueamateur.blogspot.com/2017/02/communication-entre-raspberry-pi-et.html

Utiliser les codes de ce site.
Un commentaire fourni également une bonne info :
Pour vérifier la communication j'ai ajouté coté Arduino et coté Raspberry PI la commande radio.printDetails(). Bien vérifier les adresses RX_ADDR_P0-1 coté Arduino et TXADDR coté Raspberry PI sont le mêmes. Vérifier également la vitesse Data rate.
TODO : trouver un tutoriel permettant de mettre en place la liaison radio entre la Raspberry Pi et l'Arduino.



## Environnement Python avec OpenCV

#### Le problème
Travailler en python peut sembler difficile : versions 2 et 3 installés sur son PC, différents repertoires d'installations ($ whereis python).

Il n'est pas recommandé d'utiliser directement le dossier python du système pour travailler.

Cela peut poser des problèmes lorsqu'on souhaite développer deux applications avec des versions de modules différents.

Il faut donc mettre en place un environnement virtuel dans son worksplace et y installer les modules nécessaires au projet.

cf. https://stackoverflow.com/questions/41992104/usr-bin-python-vs-usr-local-bin-python :
“If it's a virtualenv, that also makes cleanup easier; just delete the virtualenv when you no longer need it as opposed to trying to uninstall libraries installed at the system level.”


#### Installation de virtualenv : 

#### Etape 1 : installer pipx
      (cf. https://pypi.org/project/pipx/)
      (Utiliser brew sur MacOS, voir dans le lien)
      $ python3 -m pip install --user pipx
      $ python3 -m pipx ensurepath
      $ python3 -m pip install --user -U pipx
      
#### Etape 2 : installer virtualenv 
      (cf. https://virtualenv.pypa.io/en/stable/)
      $ pipx install virtualenv

#### Etape 3 : créer l'environnement virtuel dans le repertoire
      $ virtualenv -p python3 .
      OU $ virtualenv -p python3 <desired-path> (depuis ailleurs)
      $ source ./bin/activate
      OU $ source <desired-path>/bin/activate (depuis ailleurs)

#### Etape 4 : sélectionner l'environnement virtuel fraichement créé dans VSCode
En cliquant sur python en bas à gauche



## Installation d'Open CV dans l'environnement virtuel
      Après avoir mis en place le virtualenv et l'avoir sélectionné comme interpréteur dans VSCode :
      $ pip install opencv-python





# Workflow GIT
## Installer Visual Studio Code (ou pas)

# Cloner le repo distant en local

Attention, dans la section "Adding your SSH key to the ssh-agent" il y a une coquille
Ils demande de copier la clé sans préciser qu'il s'agit de la clé publique
La commande pour récupérer la clé publique n'est donc pas :
        $ cat ~/.ssh/id_ed25519
Mais
        $ cat ~/.ssh/id_ed25519.pub

Suivre le tuto pour générer la clé sur son PC à l'adresse :
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Une fois la clé ssh de son pc ajoutée sur git, taper la commande pour cloner le repo en local :
        $ git clone git@github.com:RaphyStark/Light_Painting_5A.git



## Envoyer un gros fichier sur git
  https://git-lfs.github.com/
## Créer et push un fichier
        $ git add README.md
        $ git commit -m 'modification README.md'
        $ git push
## Récupérer un dossier du master vers une branch
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
