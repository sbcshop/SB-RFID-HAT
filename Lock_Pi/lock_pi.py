from time import sleep
import RPi.GPIO as GPIO
import serial
import platform
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)


def SerialThread():
    """ This class handles Serail Port """
    # For windows
    # dev = "COM1"
    # For Linux
    # dev = "/dev/ttyS0"
    print('SerailThread started')
    if platform.system() == 'Windows':
        ser = serial.Serial("COM1", 9600, timeout=1)
    else: 
        ser = serial.Serial("/dev/ttyS0",9600,timeout=1)
    ser.flushInput()

    msg=''
    while True: 
        while ser.inWaiting() > 0:
            msg = ser.read(12)
           
        if msg != "":
            msg=msg.decode("utf-8")
            GPIO.output(17,GPIO.HIGH)
            sleep(.2)
            GPIO.output(17,GPIO.LOW)
            return msg

flag=0
if __name__ == "__main__":
    while True:
        
        id=SerialThread()
        print (id)
        if (id == '0E0097C3F6AC' and flag==0):
            flag=1
            print ("Please wait .. Processing")
            os.system('dm-tool lock')
