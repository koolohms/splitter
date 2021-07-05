#!/bin/sh
# wave-launcher.sh
# launches waves splitter process

LOGFILE=/etc/cups/postprocessing/wave.log

(
    echo "$(date "+%m%d%Y %T") : Wave online"
) > $LOGFILE

cd /
cd /home/pi/Documents/splitter
sudo python3 wave-splitter.py
cd /

(
    echo "$(date "+%m%d%Y %T) : Wave process complete. Exiting.."
) > $LOGFILE