import os
import time
import sys

originalFile = "test-pdf.pdf"
textFile = "text.txt"
newFile = "new-pdf.pdf"

#open a pdf file as read binary
fOriginal = open(originalFile, "rb")

#open a text file as write
fText = open(textFile, "wb")

#write pdf binary into text file
fText.write(fOriginal.read())

#close both files
fOriginal.close()
fText.close()

#open text file as read
fText = open(textFile, "rb")

#create a file as write binary
fNew = open(newFile, "wb")

#write contents of text file into new file
fNew.write(fText.read())

#close both files
fText.close()
fNew.close()