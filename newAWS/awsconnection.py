from mpu6050 import mpu6050
import time
import json
import os
import glob

#load up information for connection to AWS
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient("Autobrew")
myAWSIoTMQTTClient.configureEndpoint("a1ccba331h2nwv-ats.iot.us-east-1.amazonaws.com", 8883)
myAWSIoTMQTTClient.configureCredentials("/home/autobrew/newAWS/root.pem", 
	"/home/autobrew/newAWS/52bb41a1458b2921258a054b70b8de75c99a4680d9ca9d933e9e727e3730896e-private.pem.key", 
	"/home/autobrew/newAWS/52bb41a1458b2921258a054b70b8de75c99a4680d9ca9d933e9e727e3730896e-certificate.pem.crt")

#inititialize AWS connection
myAWSIoTMQTTClient.connect()

#Get the angle of the sensor
def GetGyro():
	mpu = mpu6050(0x68)
	# gets all three angle dimentions
	data = mpu.get_accel_data()
	data_string = data['y']
	return data_string

# reads the raw temperature data from the sensor
def read_temp_raw(device_file):
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

# gets the actuall temperature and returns it in C and F
def read_temp(device_file):
	lines = read_temp_raw(device_file)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw(device_file)
	equals_pos = lines[1].find('t=')
	# gets and calculates the two temperature readings
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_c, temp_f

# gets the tempurature from the sensor
def GetTemp():
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')

	# sets the device_file to be the data from the sensor
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'

	# reads the actual temperature
	temp_c, temp_f = read_temp(device_file)
	return temp_c, temp_f

def ConvertAngle(init, current):
	# convert angle reading to gravity between 0.990 - 1.170
	
	# initial reading of gravity sensor
	init = 0
	# current/Final reading of gravity sensor
	current = 0

	# live update of alcohol content
	alcoholContent = init - current
	return alcoholContent


def main():
	i= 0
	input("Press ENTER to start...")

	start = input("What is the starting gravity reading?: ")
	print(start)
	
	#print to screen and send to AWS in json format
	while True:
		angle = GetGyro()
		temp_c, temp_f = GetTemp()
		
		payloadmsg0 = "{\n"
		payloadmsg1 = " \"temp_c\": "
		payloadmsg4 = ",\n "
		payloadmsg2 = " \"angle\": "
		payloadmsg3 = "\n}"
		
		payloadmsg = "{} {} {} {} {} {} {}".format(payloadmsg0, payloadmsg1, temp_c, payloadmsg4, payloadmsg2, angle, payloadmsg3)
		payloadmsg = json.dumps(payloadmsg)
		payloadmsg_json = json.loads(payloadmsg)
		
		myAWSIoTMQTTClient.publish("device/22/data", payloadmsg_json, 1)
		
		print("Published ", i, " to the topic: device/+/data")
		i = i + 1
		
		time.sleep(5)

	print("Program ended early")
	#disconnect if loop is broken
	myAWSIoTMQTTClient.disconnect()

if __name__ == "__main__":
	main()
