# A first model running on Greengrass

## Steps

1. At the root of the repo copy `Makefile.parameters.sample` to `Makefile.parameters` and edit it with your values.

1. Go in the first directory `01-face-detection`.

1. Run `make`.

1. After the deployment is done you can view the output with: `ssh <DEVICE-IP> cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`

1. In the console subscribe to the topic `jetson/#`, it will show you everything going on with the device.

**There is currently an issue with this function that makes it freeze for around 30 seconds the first time it sees a face, however this only happens once.**

You should be able to see the results of the inference both in the topic and the video stream. Great! Now you've used the basic components of Greengrass, let's move on and start doing your own models.