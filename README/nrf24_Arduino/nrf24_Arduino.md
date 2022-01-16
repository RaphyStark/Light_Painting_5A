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


 

Attention :
Les Arduino disposent d'un régulateur de tension (SPX1117M3-L-5 Regulator) qui se chargent de stabiliser l'alimentation électrique.
En revanche, si le module est connecté directement à une chip ATmega328, il faut ajouter un condensateur.
