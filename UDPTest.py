import socket
import subprocess

UDP_IP = "10.250.23.126" # this might need to be changed to something else
UDP_PORT = 9933

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # (Internet, UDP)
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	print ("received message: ", data)
	subprocess.call(data.split())

# example of how to send data using UDP
# UDP_IP in this case is the target ip
# UDP_PORT is also the target port
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

# UDP might not work because it needs a target IP address
