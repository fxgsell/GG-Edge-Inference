# Jetson Configuration Utility

## Carrier and Enclosure Requriements

- 1 button to trigger configuration
- Camera emplacement at best, USB at worst

## Watcher Service

- Detect 5 seconds button press
- Trigger Congiuration tool

## Configuration Tool

- Set device to wifi AP:
  1. Get device ID
  1. Configure Wifi as access-point with name: TX2-DEVID
  1. Start DHCP server lisen on AP
- Configuration
  1. Set a new wifi:
  - network
  - password
  1. Reset Greengrass:
  - Stop
  - rm -r /greengrass
  - extract greengrass
  - extract certificates
  - Start