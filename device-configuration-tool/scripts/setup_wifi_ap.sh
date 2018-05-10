#!/bin/bash

BINARIES='/opt/jetson-gg-config-tool/binaries/'
#DEVID=`ifconfig wlan0 | grep wlan0 | awk '{print $5}' | sed 's/://g'`
UUID=`cat $BINARIES/uuid`

nmcli con up uuid $UUID

#nmcli d disconnect wlan0
#nmcli device wifi hotspot con-name configuration-ap ssid JTX2-$DEVID band bg 
