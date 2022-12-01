import glob
import json
import os
import time

# load up information for connection to AWS
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from mpu6050 import mpu6050

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient("Autobrew")
myAWSIoTMQTTClient.configureEndpoint(
    "a1ccba331h2nwv-ats.iot.us-east-1.amazonaws.com", 8883
)
myAWSIoTMQTTClient.configureCredentials(
    "/home/autobrew/AutoBrew/newAWS/root.pem", 
    "/home/autobrew/AutoBrew/newAWS/52bb41a1458b2921258a054b70b8de75c99a4680d9ca9d933e9e727e3730896e-private.pem.key", 
    "/home/autobrew/AutoBrew/newAWS/52bb41a1458b2921258a054b70b8de75c99a4680d9ca9d933e9e727e3730896e-certificate.pem.crt"
)

# inititialize AWS connection
myAWSIoTMQTTClient.connect()

# get the angle of the sensor
def GetGyro():
    mpu = mpu6050(0x68)
    # gets all three angle dimentions
    data = mpu.get_accel_data()
    data_string = data["y"]
    return data_string


# reads the raw temperature data from the sensor
def read_temp_raw(device_file):
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()
    return lines


# gets the actuall temperature and returns it in C and F
def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find("t=")
    # gets and calculates the two temperature readings
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


# gets the temperature from the sensor
def GetTemp():
    os.system("modprobe w1-gpio")
    os.system("modprobe w1-therm")
    # sets the device_file to be the data from the sensor
    base_dir = "/sys/bus/w1/devices/"
    device_folder = glob.glob(base_dir + "28*")[0]
    device_file = device_folder + "/w1_slave"
    # reads the actual temperature
    temp_c = read_temp(device_file)
    return temp_c


# converts the angle to the gravity scale
def ConvertAngle(current, adjustment):
    # convert angle reading to gravity between 0.990 - 1.170
    # ----- EXAMPLE/TEST ------------
    # -1 = 0.990
    # -0.8 = 0.998
    # 0 = 1.000
    # 0.2 = 1.002
    # 0.4 = 1.004
    # 0.6 = 1.006
    # 0.8 = 1.008
    # 1 = 1.010
    # 17 = 1.170
    # --------------------------------
    
    # rounds the angle to the nearest tenth
    # divides by 100 and adds 1 to convert to the gravity scale
    gravity = (round(current, 1) / 100) + adjustment
    print(gravity)
    return gravity


# calculates the appropriate ajustment for the angle convertion
def InitialReading(sAngle, sGravity):
    sGravity = float(sGravity)
    # converts the angle to the base scale
    scale = (round(sAngle, 1) / 100) + 1
    # takes the starting gravity reading & calculates the appropriate adjustment
    adjustment = (sGravity - scale) + 1
    # returns the adjustment for the angle conversion
    return adjustment


def main():
    i = 0
    # waits for input to start program
    input("Press ENTER to start...")

    # gets the starting gravity reading from user
    startGravity = input("What is the starting gravity reading?: ")

    # set current angle to starting reading
    startAngle = GetGyro()
    adjustment = InitialReading(startAngle, startGravity)

    # print to screen and send to AWS in json format
    while True:
        angle = GetGyro()
        gravity = ConvertAngle(angle, adjustment)
        temp_c = GetTemp()

        payloadmsg0 = '{\n"temp_c": '
        payloadmsg1 = ',\n"gravity": '
        payloadmsg2 = "\n}"

        payloadmsg = "{} {} {} {} {}".format(
            payloadmsg0, temp_c, payloadmsg1, gravity, payloadmsg2
        )
        payloadmsg = json.dumps(payloadmsg)
        payloadmsg_json = json.loads(payloadmsg)

        myAWSIoTMQTTClient.publish("device/22/data", payloadmsg_json, 1)

        print("Published ", i, " to the topic: device/+/data")
        i = i + 1

        time.sleep(20)

    print("Program ended early")
    # disconnect if loop is broken
    myAWSIoTMQTTClient.disconnect()


if __name__ == "__main__":
    main()
