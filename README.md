# GG-Edge-Inference

This workshop let you use AWS Greengrass with the Nvidia Jetson TX1 to run ML models prepared with Amazon SageMaker.

## Walkthrough

1. [Get started with the configuration of AWS Greengrass and your device.](./1-greengrass-configuration/)

1. [Run a first model.](./2-face-detection/)

1. [Add capability to your Edge model with the Cloud.](./3-hybrid-face-recognition/)

1. [Build your own object detection model in SageMaker.](./4-custom-object-detection/)

1. (Optional) Advanced capabilities of the Jetson with Deepstream.

## Tips

- mplayer from remote computer to view the lambda's output

  - `ssh DEVICE cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`

- mplayer on framebuffer to view the lambda's output

  - `ssh DEVICE DISPLAY=0:0 mplayer /tmp/results.mjpeg -vo fbdev -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -fs -zoom -xy 1280`