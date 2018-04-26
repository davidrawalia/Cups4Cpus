#       ***SETUP***

# Import necessary libraries
import time
import datetime
import random
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import json
from ftplib import FTP


# GPIO pin setup
GPIO.setmode(GPIO.BCM)

heater = 21
hotPump = 20
coldPump = 16
cooler = 12

TRIG = 19
ECHO = 26
pour = 13

GPIO.setup(heater, GPIO.OUT)
GPIO.setup(hotPump, GPIO.OUT)
GPIO.setup(coldPump,GPIO.OUT)
GPIO.setup(cooler,GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)


GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(pour, GPIO.IN)


GPIO.output(heater, 0)
GPIO.output(hotPump, 0)
GPIO.output(coldPump, 0)
GPIO.output(cooler, 0)

# Servo pwm setup

# Pump test

def hotPumpTest():
    while True:
        GPIO.output(hotPump, 1)
        time.sleep(4)
        GPIO.output(hotPump, 0)
        time.sleep(4)
#hotPumpTest()

# Software SPI configuration / senspor values:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
values = [0]*8



#       *** SECONDARY METHODS ***


currentTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
currentWeight = mcp.read_adc(0);
lastTare = currentWeight;

#       *** MAIN METHOD ***

# Main program loop.
while True:

    # update time
    currentTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')


#    print "Distance measurement in progress"

#    GPIO.output(TRIG, False)                 #Set TRIG as LOW
#    print "Waitng For Sensor To Settle"
#    time.sleep(2)                            #Delay of 2 seconds

#    GPIO.output(TRIG, True)                  #Set TRIG as HIGH
#    time.sleep(0.00001)                      #Delay of 0.00001 seconds
#    GPIO.output(TRIG, False)                 #Set TRIG as LOW

#    pulse_start = time.time()
#    pulse_end = time.time()

#    while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
#        pulse_start = time.time()              #Saves the last known time of LOW pulse

#    while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
#        pulse_end = time.time()                #Saves the last known time of HIGH pulse

#    pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

#    distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
#    distance = round(distance, 2)            #Round to two decimal points

#    if distance > 2 and distance < 400:      #Check whether the distance is within range
#        print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
#        waterLevel = distance
#    else:
#        print "Out Of Range"                   #display out of range

    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)

    currentWeight = values[0]
    print(str(currentWeight))

    if GPIO.input(pour)==1:
        GPIO.output(hotPump, True)
        time.sleep(15)
        GPIO.output(hotPump, False)
        lastTare=currentWeight

    # Pause for half a second.
    time.sleep(0.5)
