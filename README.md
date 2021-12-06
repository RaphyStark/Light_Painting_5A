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
