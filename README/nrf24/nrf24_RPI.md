## Environnement RaspberryPi avec NRF24L01

    $ mkdir ~/rf24libs

    $ cd ~/rf24libs

    $ git clone https://github.com/TMRh20/RF24

    $ cd ~/rf24libs/RF24

    $ ./configure

    $ sudo make install

    $ sudo apt-get install python3-dev libboost-python-dev

    $ sudo ln -s $(ls /usr/lib/arm-linux-gnueabihf/libboost_python3-py3*.so | tail -1) /usr/lib/arm-linux-gnueabihf/libboost_python3.so
    
Nous avons trouvé une erreur à cette commande \
Il faut aller trouver le bon fichier dans /usr/lib/arm-linux-gnueabihf/ \
Pour nous le fichier s'appelle libboost_python39.so \
La commande est donc pour nous : \
    
    $ sudo ln -s $(ls /usr/lib/arm-linux-gnueabihf/libboost_python39.so | tail -1) /usr/lib/arm-linux-gnueabihf/libboost_python3.so

    $ sudo apt-get install python3-setuptools

    $ cd pyRF24/

    $ python3 setup.py build

    $ sudo python3 setup.py install

    $ sudo apt-get install python3-dev python3-rpi.gpio

sources : https://github.com/nRF24/RF24/issues/615









INFOS SUR INTERNET \
https://lastminuteengineers.com/nrf24l01-arduino-wireless-communication/ \
Cette page explique le fonctionnement du module nrf24l01. \
Il compare également les deux versions de module nrf24l01 : \
-> nrf24l01 + wireless module (la version compacte que nous avons avec une antenne intégrée)\
-> nrf24l01 + PA/LNA module (version avec antenne externe et une chip pour gérer le PA/LNA & transmission-reception)\
La différence est que cette dernière version permet une transmission sur 1000m (pas utile pour notre projet).\
Il explique également comment se fait la transaction avec accusé de reception et interruption (IRQ) : \
Transaction with acknowledgement and interrupt : \
The transmitter starts a communication by sending a data packet to the receiver. \
Once the whole packet is transmitted, it waits (around 130 µs) for the acknowledgement packet (ACK packet) to receive. \
When the receiver receives the packet, it sends ACK packet to the transmitter. \
On receiving the ACK packet the transmitter asserts interrupt (IRQ) signal to indicate the new data is available. \
Il y a également un paragraphe pour les branchements : \
CTRL-F : "Wiring – Connecting nRF24L01+ transceiver module to Arduino UNO" \
Ainsi qu'un autre paragraphe pour la mise en place de l'environnement : \
CTRL-F : "RF24 Arduino Library for nRF24L01+ Module" \
Enfin, il fournit les codes pour la communication entre deux Arduinos (un transmitter et un receiver) \
CTRL-F : "Arduino Code – For Transmitter" \
CTRL-F : "Arduino Code – For Receiver" \
La dernière partie du tutoriel fournit des indications pour améliorer le dispositif si des problèmes survenaient. \
https://tlfong01.blog/2020/01/24/raspberry-pi-3-tutorial-14-wireless-pi-to-arduino-communication-with-nrf24l01/ \
https://nrf24.github.io/RF24/md_docs_linux_install.html \
http://electroniqueamateur.blogspot.com/2017/02/communication-entre-raspberry-pi-et.html \
Utiliser les codes de ce site. \
Un commentaire fourni également une bonne info : \
Pour vérifier la communication j'ai ajouté coté Arduino et coté Raspberry PI la commande radio.printDetails().  \
Bien vérifier les adresses RX_ADDR_P0-1 coté Arduino et TXADDR coté Raspberry PI sont le mêmes.  \
Vérifier également la vitesse Data rate.\
