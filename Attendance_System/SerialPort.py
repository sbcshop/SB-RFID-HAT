#! /usr/bin/python3

'''
This file contains code to receive data on serial port
'''
import RPi.GPIO as GPIO
import serial
import platform
import queue
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

def SerialThread(queue):
    """ This class handles Serail Port """
    # For windows
    # dev = "COM1"
    # For Linux
    # dev = "/dev/ttySC0"
    print('SerialThread started')
    queue = queue
    if platform.system() == 'Windows':
        ser = serial.Serial("COM1", 9600, timeout=1)
    else: 
        ser = serial.Serial("/dev/ttyS0",9600,timeout=1)
    ser.flushInput()

    msg = ''
    while True: 
        while ser.inWaiting() > 0:
            msg = ser.read(12)
            
        if msg != "":
            msg=msg.decode("utf-8")
            print (msg)
            queue.put(msg)
            GPIO.output(17,GPIO.HIGH)
            sleep(.2)
            GPIO.output(17,GPIO.LOW)
            msg = ''

        
        
