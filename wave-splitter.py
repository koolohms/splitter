# WAVE Splitter functionality
# Justin Turcotte
# Capstone
# ESE
# June 20, 2021

import os
import time

# Important paths
POS_PRINT_DEST = "/var/spool/cups-pdf/ANONYMOUS/"
RECEIPT_DIR = "/media/pi/TESTUSB/"

while True:
    pdfs = os.listdir(POS_PRINT_DEST)

    for i in range(0,len(pdfs)):
        fr = open(POS_PRINT_DEST+pdfs[i], 'rb')
        fw = open(RECEIPT_DIR+pdfs[i], 'wb')

        fw.write(fr.read()) # write pdf to NFC device

        fr.close()
        fw.close()

        os.remove(POS_PRINT_DEST+pdfs[i])
    time.sleep(1)