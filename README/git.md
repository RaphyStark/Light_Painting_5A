# Utiliser une clé ssh pour récupérer le repo sur son linux :

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
        $ git clone git@github.com:RaphyStark/Light_Painting_5A.git \
        Tester la configuration



# Envoyer un gros fichier sur git
  https://git-lfs.github.com/

# Créer et push un fichier
        $ git add README.md
        $ git commit -m 'modification README.md'
        $ git push

# Récupérer un dossier du master vers une branch
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
