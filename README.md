# GG-Edge-Inference

This workshop let you use AWS Greengrass with the Nvidia Jetson TX1 to run ML models prepared with Amazon SageMaker.

## Walkthrough

1. [Get started](./1-greengrass-configuration/README.md) with the configuration of AWS Greengrass and your device.

1. [Run a first model](./2-face-detection/README.md).

1. A custom model ?

    1. Go in SageMaker, load the notebook.jpnb blabla..

1. Shot at HPO ?

    1. Go in SageMaker, load the notebook.jpnb blabla..

## Tips

- mplayer from remote computer to view the lambda's output

  - `ssh DEVICE cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`

- mplayer on framebuffer to view the lambda's output

  - `ssh DEVICE DISPLAY=0:0 mplayer /tmp/results.mjpeg -vo fbdev -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -fs -zoom -xy 1280`