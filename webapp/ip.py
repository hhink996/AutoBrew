import netifaces as ni

ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

print(ip)
