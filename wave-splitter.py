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

# Important paths
POS_PRINT_DEST = "/var/spool/cups-pdf/ANONYMOUS/"
RECEIPT_DIR = "/media/pi/TESTUSB/"

# Thermal printer init
p = Usb(0x0416, 0x5011, 0, 0x04, 0x03)



while True:
    pdfs = os.listdir(POS_PRINT_DEST)

    for i in range(0,len(pdfs)):
        fr = open(POS_PRINT_DEST+pdfs[i], 'rb')
        fw = open(RECEIPT_DIR+pdfs[i], 'wb')

        # fw.write(fr.read()) # write pdf to NFC device

        pdf = pdftotext.PDF(fr)
        text = "\n\n".join(pdf)
        p.text(text)
        p.cut()

        fr.close()
        fw.close()

        os.remove(POS_PRINT_DEST+pdfs[i])
    time.sleep(1)