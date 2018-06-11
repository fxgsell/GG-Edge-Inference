# GG-Edge-Inference

This workshop let you use AWS Greengrass with the Nvidia Jetson TX2 to run ML models prepared with Amazon SageMaker.

## Workshop Prerequisites

This workshop requires the following:

- An active AWS Account
- The root user credentials or IAM credentials with sufficient privileges
    **TODO**: *define IAM policy required for this workshop*
- Computer/laptop with \*nix OS (such as Mac OS or Linux)
- Tested with NVidia Jetson TX2 board, but may work with other AWS Greengrass-supported devices

## Device Provisioning

For this workshop, your device will require preparation, and this can be done in one of two ways:

### Device: Automated Provisioning

If you are using the NVidia Jetson TX2 board, you can use our [automated config tool](https://github.com/zukoo/GG-Config-Tool.git). This script will automatically provision the necessary libraries for running all the labs in this workshop.

### Device: Manual Installation**

If you are not using the NVidia Jetson TX2 device for this workshop, the labs should also work on most other devices (tested on MacBook and RaspberryPi 3) assuming the following dependencies have been met:

    - Python 2.7
    - OpenCV
    - numpy (pip)
    - face_recognition (via pip) (for *Labs 2 & 3*)
    - mxnet (for *Lab 4*)

### Environment configuration

- [Lab 0: Configuration of your Cloud9 environment.](./0-environment-configuration/)

## Walk-through

This workshop is composed of the following Labs:

1. [Lab 1: Get started with the configuration of AWS Greengrass and your device.](./1-greengrass-configuration/)
1. [Lab 2: Run a first model.](./2-face-detection/)
1. [Lab 3: Add capability to your Edge model with the Cloud.](./3-hybrid-face-recognition/)
1. [Lab 4: Build your own object classification model in SageMaker.](./4-custom-object-classification/)
1. (Optional) Advanced capabilities of the Jetson with Deepstream.

## Tips

- [TODO: confirm if this is still applicable] While every effort has been made to remain compatible with more constrained devices (eg. Raspberry Pi), if you are experiencing slow performance with such as device, you can specify an extra environment variable of `DEVICE=PI` for the Lambda function to enable low performance mode and the PiCamera (it should also work for other low power devices with USB cameras)
- In order to view the video from the device:
  - use `mplayer` from a remote computer and view the video stream within the device, for example:
    `ssh DEVICE cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`
  - use `mplayer` on local device's framebuffer to view the lambda's output
    `ssh DEVICE DISPLAY=0:0 mplayer /tmp/results.mjpeg -vo fbdev -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -fs -zoom -xy 1280`
