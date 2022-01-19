Le fichier python envoi seulement la variable uL qui contient la valeur 2

radio.payloadSize = len(struct.pack("i", uL))

Permet de définir la taille de la donnée envoyée



Le fichier arduino reçoit bien la variable

radio.setPayloadSize(4);

Permet de définir la taille de la donnée à recevoir
