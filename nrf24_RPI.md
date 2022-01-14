## Environnement RaspberryPi avec NRF24L01

Suivre :: https://github.com/nRF24/RF24/issues/615
mkdir ~/rf24libs
cd ~/rf24libs
git clone https://github.com/TMRh20/RF24
cd ~/rf24libs/RF24
./configure
sudo make install
sudo apt-get install python3-dev libboost-python-dev
sudo ln -s $(ls /usr/lib/arm-linux-gnueabihf/libboost_python3-py3*.so | tail -1) /usr/lib/arm-linux-gnueabihf/libboost_python3.so    /!/
sudo apt-get install python3-setuptools
cd pyRF24/
python3 setup.py build
sudo python3 setup.py install
sudo apt-get install python3-dev python3-rpi.gpio

Si il y a une erreur à la commande ln, aller chercher le nom du fichier dans /usr/lib/arm-linux-gnu.... et remplacer dans la commande "libboost_python3-py3*.so" par le vrai nom du fichier









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