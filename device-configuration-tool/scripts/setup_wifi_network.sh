#!/bin/bash

BINARIES='/opt/jetson-gg-config-tool/binaries/'

AP_NAME=$1
AP_PASSWORD=$2

echo -n $AP_NAME > $BINARIES/ssid
echo -n $AP_PASSWORD >  $BINARIES/pwd

#nmcli device wifi connect $AP_NAME password $AP_PASSWORD
#mcli c add save yes type wifi autoconnect yes con-name AutoConf ifname wlan0 ssid $AP_NAME
