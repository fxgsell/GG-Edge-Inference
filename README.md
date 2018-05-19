# GG-Edge-Inference

This workshop let you use AWS Greengrass with the Nvidia Jetson TX1 to run ML models prepared with Amazon SageMaker.

## Prerequisites

Have you're AWS account ready.

If the device you're using has been prepared with [our config tool](https://github.com/zukoo/GG-Config-Tool.git) you can skip this the rest of this part. If you can't use the script this workshop should also work on most devices (tested on MacBook and RaspberryPi 3) as long as you have the dependencies installed.

You will need:

    - Python 2.7
    - OpenCV
    - numpy (pip)

    - face_recognition (pip) (For parts 2 & 3)
    - mxnet (For part 4)

## Walk-through

1. [Get started with the configuration of AWS Greengrass and your device.](./1-greengrass-configuration/)

1. [Run a first model.](./2-face-detection/)

1. [Add capability to your Edge model with the Cloud.](./3-hybrid-face-recognition/)

1. [Build your own object detection model in SageMaker.](./4-custom-object-detection/)

1. (Optional) Advanced capabilities of the Jetson with Deepstream.

## Tips

- I've tried to make this workshop compatible with slower devices like the Raspberry Pi, you should specify an extra environment variable to the lambda function `DEVICE=PI` to enable low performance mode and the PiCamera (it should also work for other low power devices with USB cameras).

- mplayer from remote computer to view the lambda's output

  - `ssh DEVICE cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`

- mplayer on framebuffer to view the lambda's output

  - `ssh DEVICE DISPLAY=0:0 mplayer /tmp/results.mjpeg -vo fbdev -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -fs -zoom -xy 1280`