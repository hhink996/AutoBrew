import time
import os
import glob

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
		return temp_c

# gets the temperature from the sensor
def GetTemp():
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')

	# sets the device_file to be the data from the sensor
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'

	# reads the actual temperature
	temp_c = read_temp(device_file)
	return temp_c

def main():
    temp = GetTemp()
    print("Test Data: " + str(temp))

if __name__ == "__main__":
    main()