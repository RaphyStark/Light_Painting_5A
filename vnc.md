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