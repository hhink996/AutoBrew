import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

ENDPOINT = "arn:aws:iot:us-east-1:287923911800:thing/Autobrew"
CLIENT_ID = "Autobrew"
PATH_TO_CERT = "/home/autobrew/AWS/Autobrew.cert.pem"
PATH_TO_KEY = "/home/autobrew/AWS/Autobrew.private.key"
PATH_TO_ROOT = "/home/autobrew/AWS/root-CA.crt"
MESSAGE = "Hello World"
TOPIC = "test/testing"
RANGE = 20

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
myAWSIoTMQTTClient.connect()

print('Begin Publish')

for i in range (RANGE):
    data = "{} [{}]".format(MESSAGE, i+1)
    message = {"message" : data}
    myAWSIoTMQTTClient.publish(TOPIC, json.dumps(message), 1)

print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")
t.sleep(0.1)
print('Publish End')
myAWSIoTMQTTClient.disconnect()
