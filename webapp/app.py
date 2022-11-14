from flask import Flask, render_template
from flask import Response
from mpu6050 import mpu6050
import time
import os
import glob
import json

# get the angle of the sensor
def GetGyro():
	#from mpu6050 import mpu6050
	mpu = mpu6050(0x68)
	data = mpu.get_accel_data()
	dataString = str(data['y'])
	return dataString

# reads the raw temperature data
def ReadTempRaw(deviceFile):
	f = open(deviceFile, 'r')
	lines = f.readlines()
	f.close()
	return lines

# gets the actuall temperature & returns in C & F
def ReadTemp(deviceFile):
	lines = ReadTempRaw(deviceFile)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = ReadTempRaw(deviceFile)
	equalsPos = lines[1].find('t=')
	if equalsPos != -1:
		tempString = lines[1][equalsPos+2:]
		tempC = float(tempString) / 1000.0
		tempF = tempC * 9.0 / 5.0 + 32.0
		return tempC, tempF

# gets the temperatur from the sensor
def GetTemp():
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')

	baseDir = '/sys/bus/w1/devices/'
	deviceFolder = glob.glob(baseDir + '28*')[0]
	deviceFile = deviceFolder + '/w1_slave'

	tempC, tempF = ReadTemp(deviceFile)
	return tempC, tempF


app = Flask(__name__)

# entry point into the website
# as of now, web address is pi IP
@app.route('/')
# name of the route (index for the home page)
def index():
	angle = GetGyro()
	tempC, tempF = GetTemp()
	#x = {"Angle": angle, "TempC": str(tempC), "TempF": str(tempF)}
	#inputs = json.dumps(x)
	inputs = {'Angle': angle, 'TempC': str(tempC), 'TempF': str(tempF)}
	return render_template('index.html', data=inputs)

@app.route('/data')
def data():
	angle = GetGyro()
	tempC, tempF = GetTemp()
	listObject = [angle, str(tempC), str(tempF)]
	return render_template('data.html', listToSend = listObject)

# host = '0.0.0.0' means any device can access the web app
if __name__ == '__main__':
	app.run(host = '0.0.0.0')
