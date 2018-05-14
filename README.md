# GG-Edge-Inference

Using AWS Greengrass with the Nvidia Jetson TX1 to run ML models prepared with Amazon SageMaker.

## Get started

1. Create an S3 bucket to host the models.

1. Create a lambda with the Python2.7 runtime, create an alias "latest" pointing to $LATEST.

1. In `00-greengrass-configuration` run `python3 create-greengrass-config.py --create-group GG-ML-Workshop --bucket my-greengrass-models --function demo-inference`

    - Change the 3 parameters to values of your choice (Group Name, Bucket Name and Function Name)

1. Upload the resulting **certificates.tar.gz** on your device.

1. Go back to the console and hit Deploy in your Greengrass Group. (Choose "Automatic Detection")

1. Once the deployment finished you can go look in the console or run `python3 create-greengrass-config.py --ip-address` to get the IP of your device.

You're now set to start doing some ML @Edge.

## A first model running on Greengrass

1. At the root of the repo copy `Makefile.parameters.sample` to `Makefile.parameters` and edit it with your values.

1. Go in the first directory 01-face-detection.

1. Run `make publish`

1. After the deployment is done you can view the output with: `ssh DEVICE-IP cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`

1. In the console subscribe to the topic `jetson/#`

**There is currently an issue with this function that makes it freeze for around 30 seconds the first time it sees a face, however this only happens once.**

You should be able to see the results of the inference both in the topic and the video stream. Great! Now you've used the basic components of Greengrass, let's move on and start doing your own models.

## A custom model ?

1. Go in SageMaker, load the notebook.jpnb blabla..

## Shot at HPO ?

1. Go in SageMaker, load the notebook.jpnb blabla..

## Tips

### mplayer from remote computer to view the lambda's output

`ssh DEVICE cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`

### mplayer on framebuffer to view the lambda's output

`ssh DEVICE DISPLAY=0:0 mplayer /tmp/results.mjpeg -vo fbdev -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -fs -zoom -xy 1280`