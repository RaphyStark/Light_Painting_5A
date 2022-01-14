## Environnement Python avec OpenCV

#### Le problème
Travailler en python peut sembler difficile : versions 2 et 3 installés sur son PC, différents repertoires d'installations ($ whereis python).

Il n'est pas recommandé d'utiliser directement le dossier python du système pour travailler.

Cela peut poser des problèmes lorsqu'on souhaite développer deux applications avec des versions de modules différents.

Il faut donc mettre en place un environnement virtuel dans son worksplace et y installer les modules nécessaires au projet.

cf. https://stackoverflow.com/questions/41992104/usr-bin-python-vs-usr-local-bin-python :
“If it's a virtualenv, that also makes cleanup easier; just delete the virtualenv when you no longer need it as opposed to trying to uninstall libraries installed at the system level.”


Recommande d'utiliser virtualenv quand python demande de passer en sudo (problème d'installation de librairies) :
https://askubuntu.com/questions/1268870/python-module-not-found-in-sudo-mode-ubuntu-20-04


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