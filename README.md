# SnipsTutorial

<p align="center">
  <img src="https://camo.githubusercontent.com/49ba9a98bff75e6dc20a9cc4e2f85c77ac5279e4/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6765742e646f63732e736e6970732e61692f7374617469632f696d616765732f77696b692f736e6970735f62616e6e65725f70726f642e706e67">
  
# Tutoriel &middot;[![Latest cversion](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/Davidchasseray/3-musketeers/tree/master/cash)


*  Construire son assistant vocal

Une façon facile de créer l'assistant depuis [SNIPS assistants](https://snips.ai/) et de le lancer directement depuis le terminal.




## Installations

Dans un premier temps il sera necessaire de connecter une raspberry Pi à notre PC en utilisant une commande necessitant l'adresse ip. Il faut tout d'abord connecter la raspberry à l'aide d'un cable rg-45


Depuis un bash ubuntu si possible pour utiliser la commende "ssh".
```
> sudo ssh pi@169.254.42.42
```

Il faut alors installer docker sur la raspberry Pi

```
> curl -sSL get.docker.com | sh
```


Maintenant que la raspberry pi est connectée et que docker y est installé. 
Il faut ouvrir une nouvelle invite de commande pour transférer des fichiers qui auront étés clonés depuis [GitHub](https://github.com/neallausson/SnipsTutorial/tree/master/SNIP%20TD) 


Pour démarrer SNIPS il faut utiliser l'image docker disponible sur GitHub et la lancer depuis la raspberry pi.

* Transfert du dockerFile

Supposant que votre dossier SNIPS_TD se trouve sur votre bureau
```
> scp -r ~/Desktop/SNIPS_TD/docker pi@<169.254.42.42>:/home/pi/.
```


Puis démarrer ce dockerfile Dans le même dossier que le fichier "docker-compose.yml" grâce à : 
```
> docker-compose build
```

A partir de là, vous devriez pouvoir tester le fichier test.py depuis votre ordinateur.
```
> python3 test.py
```
## Mise ne place d'un second assistant

* Dans un premier temps il faut créer un assistant depuis le site internet de [SNIPS](https://console.snips.ai/assistants/proj_9MBdrbdxddo?store=1)

Il faudra créer un compte pour accéder à la création d'assistants. 

Une fois l'assistant créé, le télécharger puis le dezipper.

 * Transfert de l'assistant de test

 Supposant que votre dossier assistant se trouve sur votre bureau
```
> scp -r ~/Desktop/assistant pi@<169.254.42.42>:/home/pi/.
```


Il faut alors le placer au bon endroit depuis la raspberry Pi 
```
> sudo rm -r /home/pi/docker/assistant
> sudo mv /home/pi/assistant /home/pi/docker/assistant
```

Alors on peut relancer SNIPS
```
> docker-compose build
```

Maintenant vérifions que les bons fichiers sont au bons endroits :

```
> cd /usr/share/snips/assistant
> ls

assistant.json  dataset.json  trained_assistant.json custom_asr/ custom_hotword/
```

## Utilisation
* Utilisiation des scripts python pour gérer un lecteur de musique :

Créer unn fichier musicPlayer.py et le modifier à l'aide d'un éditeur de texte.

Il faudra utiliser des assets tels que pygame ou encore mqtt. 

Ainsi il faut avant cela rentrer ces lignes de commande : 
```
> pip install paho-mqtt
> pip install pygame
```

Puis éditer musicPlayer.py:
```python
import paho.mqtt.client as mqtt
import pygame as py

HOST = '169.254.42.42'
PORT = 1883

py.init()



def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    # Subscribe to the hotword detected topic
    client.subscribe("hermes/hotword/default/detected")
    # Subscribe to intent topic
    client.subscribe('hermes/intent/nextSong')
    # Subscribe to intent topic
    client.subscribe('hermes/intent/previousSong')
    # Subscribe to intent topic
    client.subscribe('hermes/intent/resumeMusic')
    # Subscribe to intent topic
    client.subscribe('hermes/intent/speakerInterrupt')

def on_message(client, userdata, msg):
    global stop
    global compteur
    global music
    #print("Message received on topic {0}: {1}".format(msg.topic, msg.payload))
    print (msg)
    if msg.topic == 'hermes/hotword/default/detected':
        print("Hotword detected!")

    elif msg.topic == 'hermes/intent/nextSong':
        print("chanson suivante!")
        compteur = (compteur+1)%len(music);
        py.mixer.music.load(music[compteur]);
        py.mixer.music.play(loops=0,start = 0.0);
        stop = False;

    elif msg.topic == 'hermes/intent/previousSong':
        print("chanson previous!")
        compteur = (compteur-1)%len(music);
        py.mixer.music.load(music[compteur]);
        py.mixer.music.play(loops=0,start = 0.0);
        stop = False;

    elif msg.topic == 'hermes/intent/resumeMusic':
        print("chanson play!")
        if(stop == False):
            py.mixer.music.play(loops=0,start = 0.0)
        else:
            stop = False;
            py.mixer.music.unpause();

    elif msg.topic == 'hermes/intent/speakerInterrupt':
        print("chanson stop!")
        if(stop == False):
            py.mixer.music.pause();
            stop =True;

compteur = 0;
stop = False;
music = ['Unravel.ogg','JeSuis.ogg','LaLumière.ogg','Waxx.ogg','YeuxDisent.ogg'];
py.mixer.music.load(music[compteur]);

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)
client.loop_forever()

```

Pour tester le code, s'assurer que SNIPS tourne sur la raspberry Pi et executer la commande :
```sh
> python3 musicPlayer.py
```

Vous pouvez désormais créer votre propre assistant vocal à l'aide de SNIPS

## pip Dependencies 

- [pigame](https://www.pygame.org/news)
- [mqtt](http://mqtt.org/)


## Thanks:

- [fixer.io](http://fixer.io/) 

- [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#set-up-the-repository)

- [SNIPSco](https://snipsco.github.io/sam/tutorials/mqtt-python)

- [SNIPSco doc](https://github.com/snipsco/snips-platform-documentation/wiki/2.-Create-an-assistant-using-an-existing-bundle)


- [hermes protocol](https://github.com/snipsco/snips-platform-documentation/wiki/6.--Miscellaneous#hermes-protocol)


- [SNIPS](https://snips.ai/)
