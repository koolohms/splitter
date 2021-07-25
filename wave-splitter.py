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
usbOK = False
p = None
while not usbOK:
    try:
        p = Usb(0x0416, 0x5011, 0, 0x04, 0x03)
    except:
        print("USB Error: Check that the USB printer is connected and powered on.")
        time.sleep(1)
    else:
        print("USB Note: USB printer has been detected.")
        usbOK = True


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
            fr = open(POS_PRINT_DEST+pdfs[i], 'rb')
            pdf = pdftotext.PDF(fr)

            if state == 0:
                receiptSent = False
                fr.seek(0,0)    #let's go back to the beginning of the file
                while not receiptSent:
                    try:
                        fw = open(RECEIPT_DIR+pdfs[i]+".txt", 'wb')
                    except:
                        print("NFC Error: unable to access NFC device.")
                        time.sleep(1)
                    else:
                        print("NFC Info: receipt sent to NFC device.")
                        receiptSent = True
                fw.write(fr.read()) # write pdf to NFC device
                fw.close()

            elif state == 1:
                receiptPrinted = False
                text = "\n\n".join(pdf)
                while not receiptPrinted:
                    try:
                        p.text(text)
                        p.cut()
                    except:
                        print("USB Error: there is an issue printing to the USB printer. Attempting to reconnect printer...")
                        p = Usb(0x0416, 0x5011, 0, 0x04, 0x03)
                        time.sleep(1)
                    else:
                        print("USB Info: receipt printed to USB printer.")
                        receiptPrinted = True
        except:
            fr.close()
            i -= 1
            time.sleep(1)
            print("[ERROR]: Exception raised!")

        else:
            fr.close()

            try:
                os.remove(POS_PRINT_DEST+pdfs[i])
            except:
                print("[ERROR] Could not remove file: ", POS_PRINT_DEST+pdfs[i])
            else:
                pass

    time.sleep(1)