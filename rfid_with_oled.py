from oled_091 import SSD1306
from subprocess import check_output
from time import sleep
from datetime import datetime
from os import path
import serial
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)

DIR_PATH = path.abspath(path.dirname(__file__))
DefaultFont = path.join(DIR_PATH, "Fonts/GothamLight.ttf")


class read_rfid:
    def read_rfid (self):
        ser = serial.Serial ("/dev/ttyS0")                           #Open named port 
        ser.baudrate = 9600                                            #Set baud rate to 9600
        data = ser.read(12)                                            #Read 12 characters from serial port to data
        if(data != " "):
            GPIO.output(17,GPIO.HIGH)
            sleep(.2)
            GPIO.output(17,GPIO.LOW)
        ser.close ()                                                   #Close port
        data=data.decode("utf-8")
        return data


def info_print():

    # display.WhiteDisplay()
    display.DirImage(path.join(DIR_PATH, "Images/SB.png"))
    display.DrawRect()
    display.ShowImage()
    sleep(1)
    display.PrintText("Place your TAG", FontSize=14)
    display.ShowImage()
    

display = SSD1306()
SB = read_rfid()



if __name__ == "__main__":
    info_print()
    while True:
        id=SB.read_rfid()
        print (id)
        #CPU = info.CPU_Info()
        # display.DirImage("Images/CPU.png", size=(24, 24), cords=(0, 0))
        display.PrintText("ID : " +(id), cords=(4, 8), FontSize=11)
        display.DrawRect()
        display.ShowImage()
        sleep(2)
        display.PrintText("Place your TAG", FontSize=14)
        display.ShowImage()
        
        
