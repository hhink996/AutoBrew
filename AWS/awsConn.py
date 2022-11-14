from mpu6050 import mpu6050
import time
import os
import glob
from awscrt import mqtt
import sys
import threading
from uuid import uuid4
import json
import paho.mqtt.client as paho
import socket
import ssl
import string

connflag = False

def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()
mqtt.on_connect = on_connect
mqttc.on_message = on_message

awshost = "arn:aws:iot:us-east-1:287923911800:thing/Autobrew"
awsport = 8883
clientId = "Autobrew"
thingName = "Autobrew"
caPath = "/home/autobrew/AutoBrew/AWS/certifications/AmazonRootCA1.pem"
certPath = "/home/autobrew/AutoBrew/AWS/certifications/Autobrew.certpem"
keyPath = "/home/autobrew/AutoBrew/AWS/certifications/Autobrew.private.key"

#mqttc.tls.set(caPath, certificate=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

mqtt.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

def GetGyro():
    mpu = mpu6050(0x68)
    data = mpu.get_accel_data()
    data_string = str(data['y'])
    return data_string

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(deivce_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def GetTemp():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1/slave'
    temp_c, temp_f = read_temp(device_file)
    return temp_c, temp_f

while True:
    if connflag == True:
        temp_c, temp_f = GetTemp()
        angle = GetGyro()

        payloadmsg0 = "{"
        payloadmsg1 = " \"temp_c\": \""
        payloadmsg2 = " \"angle\": \""
        payloadmsg3 = "\"}"

        payloadmsg = "{} {} {} {}".format(payloadmsg0, payloadmsg1, temp_c, payloadmsg2, angle, payloadmsg3)
        payloadmsg = json.dumps(payloadmsg)
        payloadmsg_json = json.loads(payloadmsg)

        mqttc.publish("Autobrew", payloadmsg_json, qos=1)

    else:
        print("Waiting for connection...")

        #print("Gyro : " + angle)
        #print("Temp : " + str(temp_c) + " " + str(temp_f) + '\n')
        time.sleep(1)
