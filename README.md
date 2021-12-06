# README master

#### Hello team Light Painting




## Envoyer un gros fichier sur git
  https://git-lfs.github.com/


## Créer et push un fichier
        $ git add README.md
        $ git commit -m 'modification README.md'
        $ git push


## Comment récupérer un dossier du master vers une branch
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



## Mettre en place un environnement local

#### Le problème
Quand on code en python, on se retrouve avec beaucoup de problèmes.
Il y a deux versions : la 2 et la 3, mais aussi plusieurs enplacements.
Travailler en python peut sembler difficile : versions 2 et 3 installés sur son PC, différents repertoires d'installations ($ whereis python)
Il n'est pas recommandé d'utiliser directement le dossier python du système pour travailler.
Cela peut poser des problèmes lorsqu'on souhaite développer deux applications avec des versions de modules différents.
Il faut donc mettre en place un environnement virtuel dans son worksplace et y installer les modules nécessaires au projet.
cf. https://stackoverflow.com/questions/41992104/usr-bin-python-vs-usr-local-bin-python :
“If it's a virtualenv, that also makes cleanup easier; just delete the virtualenv when you no longer need it as opposed to trying to uninstall libraries installed at the system level.”
“If it's a virtualenv, that also makes cleanup easier; just delete the virtualenv when you no longer need it as opposed to trying to uninstall libraries installed at the system level.”


#### Installation de virtualenv : 

## Etape 1 : installer pipx
https://pypi.org/project/pipx/
      $ python3 -m pip install --user pipx
      $ python3 -m pipx ensurepath
      $ python3 -m pip install --user -U pipx
      
## Etape 2 : installer virtualenv 
      https://virtualenv.pypa.io/en/stable/
      $ pipx install virtualenv

## Etape 3 : créer l'environnement virtuel dans le repertoire
      $ virtualenv -p python3 .
      $ virtualenv -p python3 <desired-path> (depuis ailleurs)
      $ source ./bin/activate
      $ source <desired-path>/bin/activate (depuis ailleurs)

## Etape 4 : sélectionner l'environnement virtuel fraichement crée depuis VSCode
En cliquant sur python en bas à gauche
