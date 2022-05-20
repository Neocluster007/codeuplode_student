import paho.mqtt.client as paho
import random

import sys
import os


broker="broker.mqttdashboard.com"
port=1883

path  = "/home/pi/MAASProject/"
clone = "git clone gitolite@<server_ip>:/your/project/name.git"

def on_message(client, userdata, message):
    global data_str_number

    data = str(message.payload.decode("utf-8"))
    print("message received ", data)
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

    if(data == "download"):
        os.system("sudo mkdir /home/pi/testdownload")
        os.system("sudo rm -rf /home/pi/testdownload/codeuplode_student && cd /home/pi/testdownload && git clone https://github.com/ballbuen19/codeuplode_student.git && mv /home/pi/testdownload/codeuplode_student/* /home/pi/MAASProject")
        #os.system("sudo reboot")

        #os.chdir(path)  # Specifying the path where the cloned project needs to be copied
        #os.system(clone)  # Cloning



r1 = random.randint(5, 15000)
client1= paho.Client("AutoUpdateCode_"+str(r1))
client1.connect(broker,port)
client1.on_message=on_message
client1.subscribe("MAAS/Project_SmartPost/CMD")

print("Auto Download Ready")

while True:
    client1.loop_start()
