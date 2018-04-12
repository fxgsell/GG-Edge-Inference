#!/bin/sh

nmcli d disconnect wlan0

BINARIES='/opt/jetson-gg-config-tool/binaries/'

SSID=`cat $BINARIES/ssid`
PWD=`cat $BINARIES/pwd`

nmcli device wifi con $SSID password $PWD
#Check output restart AP if Failed