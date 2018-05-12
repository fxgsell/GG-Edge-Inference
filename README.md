# GG-Edge-Inference

Using AWS Greengrass with the Nvidia Jetson TX1 to run ML models prepared with Amazon SageMaker.

## Tips

### mplayer to view the lambda's output

`mplayer –demuxer lavf -lavfdopts format=mjpeg:probesize=32 /tmp/ssd_results.mjpeg`

### mplayer from remote computer to view the lambda's output

`ssh DEVICE cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`

### mplayer on framebuffer to view the lambda's output

`ssh DEVICE DISPLAY=0:0 mplayer /tmp/results.mjpeg -vo fbdev -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -fs -zoom -xy 1280`