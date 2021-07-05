#!/bin/sh
# wave-launcher.sh
# launches waves splitter process

LOGFILE=/home/pi/wave.log
PYTHONFILE=/home/pi/Documents/splitter

(
    echo "$(date "+%m%d%Y %T") : Wave online"
) > $LOGFILE

cd /
cd $PYTHONFILE
sudo python3 wave-splitter.py
cd /

(
    echo "$(date "+%m%d%Y %T") : Wave process complete. Exiting.."
) > $LOGFILE