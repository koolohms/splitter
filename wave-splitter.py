# WAVE Splitter functionality
# Justin Turcotte
# Capstone
# ESE
# June 20, 2021

# Printer information
# Vendor ID:Product Code = 0416:5011
# Interface number = 4
# Output endpoint address = 3

import os
import time
import sys
escposModulePath = "/home/pi/.local/lib/python3.7/site-packages"
sys.path.append(escposModulePath)
from escpos.printer import Usb
import pdftotext
import RPi.GPIO as GPIO

# Important paths
POS_PRINT_DEST = "/var/spool/cups-pdf/ANONYMOUS/"
RECEIPT_DIR = "/media/pi/TESTUSB/"

# Thermal printer init
p = Usb(0x0416, 0x5011, 0, 0x04, 0x03)

# GPIO
# 0 -> NFC device
# 1 -> Printer device
GPIO_PIN = 25   # We're using GPIO "BCM 25"
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

# Wait for NFC device to be ready
while not os.path.isdir(RECEIPT_DIR):
    time.sleep(1)

while True:
    pdfs = os.listdir(POS_PRINT_DEST)

    for i in range(0,len(pdfs)):
        state = GPIO.input(GPIO_PIN)

        try:
            pdf = pdftotext.PDF(fr)

            fr = open(POS_PRINT_DEST+pdfs[i], 'rb')

            if state == 0:
                fw = open(RECEIPT_DIR+pdfs[i], 'wb')
                fw.write(fr.read()) # write pdf to NFC device
                fw.close()

            elif state == 1:
                text = "\n\n".join(pdf)
                p.text(text)
                p.cut()
        except:
            fr.close()
            i -= 1
            time.sleep(1)

        else:
            fr.close()
            os.remove(POS_PRINT_DEST+pdfs[i])

    time.sleep(1)