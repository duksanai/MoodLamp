#!/usr/bin/python
import time
#import schedule
import os
from threading import Thread, Event
import RPi.GPIO as GPIO
#import ColorCustom as CC
GPIO.setmode(GPIO.BCM)  # choose BCM numbering scheme.

#light_sensor = 4
event = Event() #thread end event

#GPIO.setup(light_sensor, GPIO.IN)# set GPIO 4 as input for light sensor
GPIO.setup(17, GPIO.OUT)# set GPIO 17 as output for white led  
GPIO.setup(27, GPIO.OUT)# set GPIO 27 as output for red led  
GPIO.setup(22, GPIO.OUT)# set GPIO 22 as output for red led
GPIO.setwarnings(False)

hz = 50
bright = 50
autoBrightCheck = False
redC = 0
redC_ = 0
blueC = 0
blueC_ = 0
greenC = 0
greenC_ = 0
wCode = 0

red = GPIO.PWM(17, hz)    # create object red for PWM on port 17  
green = GPIO.PWM(27, hz)      # create object green for PWM on port 27   
blue = GPIO.PWM(22, hz)      # create object blue for PWM on port 22 

red.start(0)
green.start(0)
blue.start(0)

def ColorChange(r, g, b, bright): #color change
    global redC_, greenC_, blueC_
    brightness = float(bright) / 100
    if redC_ < r:
        redC_ = redC_ + 1
    elif redC_ > r:
        redC_ = redC_ - 1
    if greenC_ < g:
        greenC_ = greenC_ + 1
    elif greenC_ > g:
        greenC_ = greenC_ - 1
    if blueC_ < b:
        blueC_ = blueC_ + 1
    elif blueC_ > b:
        blueC_ = blueC_ - 1
    red.ChangeDutyCycle(redC_ * brightness)
    green.ChangeDutyCycle(greenC_ * brightness)
    blue.ChangeDutyCycle(blueC_ * brightness)
    
def BrControl(): #brightness control
    global bright, autoBrightCheck
    while True: #hand control in app
        bright = input('brightness: ')
        time.sleep(0.01)
        if autoBrightCheck == True:
            break
        if event.is_set():
            return
    while True: #auto control from sensor
        #bright = from sensor --> need calculate
        if autoBrightCheck == False:
            break
        if event.is_set():
            return
    
def Weather():
    global wCode, redC, greenC, blueC
    while True:
        wCode = wCode + 1
        if wCode == 1: #sunny
            #sunny(
            redC = 0
            greenC = 100
            blueC = 0
        elif wCode == 2: #cloudy
            redC = 100
            greenC = 100
            blueC = 0
        elif wCode == 3: #rainy
            redC = 0
            greenC = 0
            blueC = 100
        elif wCode == 4: #snowy
            redC = 0
            greenC = 100
            blueC = 100
        else:
            wCode = 0
        time.sleep(5)
        if event.is_set():
            return
    
sensorTh = Thread(target=BrControl)
weatherTh = Thread(target=Weather)
sensorTh.start()
weatherTh.start()

try:
    while True:
        #autoBrightCheck = check value from app
        ColorChange(redC, greenC, blueC, bright)
        time.sleep(0.005)
  
except KeyboardInterrupt: #When 'Ctrl + c' / turn off
    red.stop()		#stop red led
    green.stop()    #stop green led
    blue.stop() 	#stop blue led
    event.set()		#stop light sensor thread
    GPIO.cleanup()  # clean up GPIO on CTRL+C exit 
