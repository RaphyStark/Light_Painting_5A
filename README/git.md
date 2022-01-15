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

Si la clé est demandée après chaque commande git pour accéder au server (fetch, pull, push...) :
        
        $ ssh-add ~/.ssh/id_ed2551

Réponse trouvée sur ce topic :
https://superuser.com/questions/988185/how-to-avoid-being-asked-enter-passphrase-for-key-when-im-doing-ssh-operatio



        $ git commit -a will commit all tracked files, not track untracked files
        $ git add . will track untracked files in the current directory
        $ git add -a will track all untracked files


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
