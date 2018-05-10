#!/bin/bash

BINARIES='/opt/jetson-gg-config-tool/binaries/'
DEVID=`ifconfig wlan0 | grep wlan0 | awk '{print $5}' | sed 's/://g'`

mkdrir -p $BINARIES
cd $BINARIES

# DL root
# DL greegrass

WIFI_NAME=JTX2_$DEVID
nmcli connection add type wifi ifname '*' con-name conf-hotspot autoconnect no ssid $WIFI_NAME 
nmcli con modify conf-hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
#nmcli con modify Hostspot wifi-sec.key-mgmt wpa-psk
#nmcli con modify Hostspot wifi-sec.psk "veryveryhardpassword1234"

UUID=$(grep uuid /etc/NetworkManager/system-connections/conf-hotspot | cut -d= -f2)
echo -n UUID > uuid

