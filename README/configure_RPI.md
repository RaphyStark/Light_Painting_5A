## Branchements
http://electroniqueamateur.blogspot.com/2017/02/communication-entre-raspberry-pi-et.html

## Environnement virtuel LightPainting
https://opensource.com/article/21/2/python-virtualenvwrapper

    $ sudo pip3 install virtualenvwrapper
    
    $ gedit .bashrc

Ajouter à la fin les lignes suivantes :\
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 \
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv \
source /usr/local/bin/virtualenvwrapper.sh

Création d'un environnement virtuel (attention à ne pas de ajouter de "-" cf.setup.py de RF24)

    $ mkvirtualenv LightPainting --always-copy
    
L'option --always-copy assure (à vérifier) que le virtualenv créer bien les lib dans le virtualenv

    $ cd LightPainting
    
## Installation de RF24 depuis les sources sur la RaspberryPi

    $ mkdir rf24libs

    $ cd rf24libs

    $ git clone https://github.com/TMRh20/RF24

    $ cd RF24

    $ ./configure --prefix=/home/pi/.virtualenvs/LightPainting/bin

L'option --prefix permet d'indiquer à ./configure où installer la lib \
On remarquera plus loin à la fin de la commande sudo python3 setup.py install : \
librf24.so found at /home/pi/.virtualenvs/LightPainting/bin/lib \
Et à la fin de la commande sudo make install : \
Installing Libs to /home/pi/.virtualenvs/light-painting/bin/lib

    $ sudo make install

    $ sudo apt-get install python3-dev libboost-python-dev

    $ sudo ln -s $(ls /usr/lib/arm-linux-gnueabihf/libboost_python39.so | tail -1) /usr/lib/arm-linux-gnueabihf/libboost_python3.so

    $ sudo apt-get install python3-setuptools

    $ cd pyRF24/

    $ /home/pi/.virtualenvs/LightPainting/bin/python3.9 setup.py build

    $ sudo /home/pi/.virtualenvs/LightPainting/bin/python3.9 setup.py install

    $ sudo apt-get install python3-dev python3-rpi.gpio


## Installation de OpenCV sur la Raspberry Pi (toujours dans l'environnement virtuel)

    $ pip3 install opencv-python -v

L'option -v permet de voir où en est l'installation qui peut être assez longue



sources : \
https://github.com/nRF24/RF24/issues/615
