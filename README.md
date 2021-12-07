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
Bien que le lien suivant est une impasse, il fournit les schémas des branchements des modules :
https://forums.framboise314.fr/viewtopic.php?f=44&t=1284
D'abord la librairie libjson0-dev n'existe plus.
Et lorsqu'on la remplace par libjson11-1 (ou encore libjson11-1-dev), on obtient une nouvelle erreur lors de l'execution de la commande make.
Pour corriger cette dernière erreur, il faut changer l'import dans le fichier sender.cpp que le tutoriel demande de télécharger.
L'erreur relative à l'import du json disparait mais de nouvelles aparaissent.
Il semblerait donc que ce tutoriel a été mis en place avec une version trop ancienne de json et qu'il serait alors plus utilisable.



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
## Installer Visual Studio Code
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
