from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys

myMQTTClient = AWSIoTMQTTClient("dojodevice1")

myMQTTClient.configureEndpoint("arn:aws:iot:us-east-1:287923911800:thing/Autobrew", 8883)
myMQTTClient.configureCredentials("/home/autobrew/AWS/Autobrew.cert.pem","/home/autobrew/AWS/Autobrew.private.key", "./Autobrew.pem.crt.txt")

myMQTTClient.connect()
print("Client Connected")

msg = "Sample data from the device";
topic = "general/inbound"
myMQTTClient.publish(topic, msg, 0)
print("Message Sent")

myMQTTClient.disconnect()
print("Client Disconnected")
