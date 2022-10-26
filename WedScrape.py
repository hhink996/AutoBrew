#******************************************************************#
#                                                                  #
# Made by Matthew Lingenfelter                                     #
# WebScrap.py                                                      #
# Gets the data from the website that the raspberry pi is hosting  #
#                                                                  #
#******************************************************************#
from urllib.request import urlopen
import re
import time

# Gets the IP of the pi from the user
def GetIp():
    ip = input('What is the IP address of your Pi?\n')
    return ip

# Goes to the pi's website and returns the html text
def GetHTML(ip):
    # Opens the website with the data from the raspberry pi
    first = "http://"
    last = ":5000/data"
    url = first + ip + last
    page = urlopen(url)

    # Gets and decodes the html text
    htmlBytes = page.read()
    html = htmlBytes.decode("utf-8")
    return html

# Gets the header from the website
def GetHeader(html):
    # Gets the header of the webpage
    headerIndex = html.find("<h1>")
    startIndex = headerIndex + len("<h1>")
    endIndex = html.find("</h1>")
    header = html[startIndex:endIndex]
    return header

# Gets the raw data from the website
def GetData(html):
    # Gets all the data from the webpage
    p1Index = html.find("<p>")
    startIndex = p1Index + len("<p>")
    endIndex = html.find("</body>")
    rawData = html[startIndex:endIndex]
    return rawData

# Gets the raw data from the html text and refines it
def RefineData(rawData):
    # Extracts just the data from the html text
    temp = rawData.split("\t")
    data = []
    data.append(temp[0])
    data.append(temp[5])
    data.append(temp[10])
    for x in range(len(data)):
        data[x] = data[x].replace("<p>", "")
        data[x] = data[x].replace("</p>", "")
        data[x] = data[x].replace("\n", "")

    # Converts the data from strings to floats
    angle = float(data[0])
    tempC = float(data[1])
    tempF = float(data[2])

    # Rounds the data
    angle = round(angle, 3)
    tempC = round(tempC)
    tempF = round(tempF)
    return angle, tempC, tempF

# Main function that gets and prints the data from the website every 20 seconds
def main():
    ip = GetIp()
    html = GetHTML(ip)
    header = GetHeader(html)
    rawData = GetData(html)
    angle, tempC, tempF = RefineData(rawData)
    print(header + "...\n" + str(angle) + "\n" + str(tempC) + "\n" + str(tempF))
    time.sleep(20)

    # continuously get and print the data from the website, every 20 seconds
    while True:
        html = GetHTML(ip)
        rawData = GetData(html)
        angle, tempC, tempF = RefineData(rawData)
        print("\n" + str(angle) + "\n" + str(tempC) + "\n" + str(tempF))
        time.sleep(20)

if __name__ == "__main__":
    main()