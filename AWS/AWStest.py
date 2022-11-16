import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform
import json
import logging

logging.basicConfig(level = logging.INFO)

class PupSub(object):
    def __init__(self, listener = False, topic = "default"):
        self.connect = False
        self.listener = listener
        self.topic = topic
        self.logger = logging.getLogger(repr(self))

    def __on_connect(self, client, userdata, flags, rc):
        self.connect = True

        if self.listener:
            self.mqttc.subscribe(self.topic)

        self.logger.debug("{0}".format(rc))

    def __on_message(self, client, userdata, msg):
        self.logger.info("{0}, {1} - {2}".format(userdata, msg.topig, msg.payload))

    def __on_log(self, client, userdata, level, buf):
        self.logger.debug("{0}, {1}, {2}, {3}".format(client, userdata, level, buf))

    def bootstrap_mqtt(self):
        self.mqttc = paho.Client()
        self.mqttc.on_connect = self.__on_connect
        self.mqttc.on_message = self.__on_message
        self.mqttc.on_log = self.__on_log

        awshost = "arn:aws:iot:us-east-1:287923911800:thing/Autobrew"
        awsport = 8883

        caPath = "/home/autobrew/AutoBrew/AWS/certifications/AmazonRootCA1.pem"
        certPath = "/home/autobrew/AutoBrew/AWS/certifications/Autobrew.certpem"
        keyPath = "/home/autobrew/AutoBrew/AWS/certifications/Autobrew.private.key"

        self.mqttc.tls_set(caPath,
            certfile=certPath,
            keyfile=keyPath,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2,
            ciphers=None)

        result_of_connection = self.mqttc.connect(awshost, awsport, keepalive=120)

        if result_of_connection == 0:
            self.connect = True

        return self

    def start(self):
        self.mqttc.loop_start()

        while True:
            sleep(2)
            if self.connect == True:
                self.mqttc.publish(self.topic, json.dumps({"message": "Hello COMP680"}), qos=1)
            else:
                self.logger.debug("Attempting to connect.")

if __name__ == '__main__':
    PupSub(listener = True, topic = "chat-evets").bootstrap_mqtt().start()