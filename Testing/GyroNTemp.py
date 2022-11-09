from mpu6050 import mpu6050
import time
import os
import glob

# get the angle from the sensor
def GetGyro():
	# sets mpu as the physical sensor
	mpu = mpu6050(0x68)
	# gets all three angle dimentions
	# accel_data is actually gyro_data
	data = mpu.get_accel_data()
	# sets the correct dimention to a string
	data_string = str(data['x'])
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

# *FOR NOW* runs untill forced stop
while True:
	# gets the angle and prints it
	angle = GetGyro()
	print("Gyro : " + angle)
	# gets the temperatures and prints them
	temp_c, temp_f = GetTemp()
	print("Temp : " + str(temp_c) + ", " + str(temp_f) + '\n')
	time.sleep(1)
