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
