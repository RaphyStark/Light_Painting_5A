## Environnement virtuel Python avec OpenCV

      $ python3 -m pip install --user pipx
      $ python3 -m pipx ensurepath
      Ouvrir un nouveau terminal pour que les changements prennent effet
      $ python3 -m pip install --user -U pip
      $ pipx install virtualenv
      Se déplacer dans le dossier ou installer l'environnement virtuel
      $ cd Light_Painting_5A/raspberry_codes/trajectoire
      $ mkdir virtualenv
      $ cd virtualenv
      $ virtualenv -p python3 .
      $ source ./bin/activate
      A ce moment, le nom du repertoire est écrit avant la ligne de commande
      $ pip install opencv-python -vv
      L'installation sur Raspberry Pi 3 B+ prend environ 2h (prévoir un long café...)




#### Pourquoi installer un environnement virtuel ?
Travailler en python peut sembler difficile : versions 2 et 3 installés sur son PC, différents repertoires d'installations ($ whereis python)...

Il n'est pas recommandé d'utiliser directement l'installation python du système pour travailler.
De plus, on peut s'y perdre facilement (plusieurs repertoires d'installations, Python, Python3...)

Cela peut poser des problèmes lorsqu'on souhaite développer deux applications avec des versions de modules différents.

Il faut donc mettre en place un environnement virtuel dans son worksplace et y installer les modules nécessaires au projet.

cf. https://stackoverflow.com/questions/41992104/usr-bin-python-vs-usr-local-bin-python :
“If it's a virtualenv, that also makes cleanup easier; just delete the virtualenv when you no longer need it as opposed to trying to uninstall libraries installed at the system level.”

Il est également recommandé d'utiliser un environnement virtuel lorsque l'utilisation de certains modules nécessitent une élevation de droits :
https://askubuntu.com/questions/1268870/python-module-not-found-in-sudo-mode-ubuntu-20-04

