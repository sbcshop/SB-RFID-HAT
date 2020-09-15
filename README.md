# SB-RFID-HAT
This is a Raspberry Pi RFID HAT based on EM18 module operating in the 125Khz frequency range. It supports two communication interfacs: UART for RFID and I2C for Oled Display.

## Features

* Standard Raspberry Pi 40PIN GPIO extension header, supports Raspberry Pi series boards
* Two interface options: UART for RFID, I2C for Oled Display
* User configurable buzzer (connected on GPIO  of Raspberry pi)

## How To configure ? 

### Enable i2c interface

I2C interface is disable by default in Raspberry Pi, To enable it type below command.

``` sudo raspi-config ```

* Now select Interfacing option.
* Now we need to select I2C option.
* Now select Yes and press enter and then ok.

After this step reboot raspberry by typing below command:

``` sudo reboot ```

### Install Required Libraries

* sudo apt-get install python-smbus
* sudo apt-get install i2c-tools

To verify the kist of connected device on I2C interface, you can run below commond :

``` sudo i2cdetect -y 1 ```

### Install Adafruit Python Library for OLED display module (Only required if you want to use oled display)

``` git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git ```

``` cd Adafruit_Python_SSD1306 ```

``` sudo python3 setup.py install ```

### How to run SB-PI-HAT examples

To run examples of SB-PI-HAT, clone this repository by executing below command

``` git clone https://github.com/sbcshop/SB-RFID-HAT.git ```

``` cd SB-RFID-HAT ```

``` python3 rfid.py ``` (Without Oled display, output on terminal/shell)

         or
 
``` python3 rfid_with_oled.py ``` ( To show detected tag id on Oled as well as on terminal/shell)

