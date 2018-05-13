# GG-Edge-Inference

Using AWS Greengrass with the Nvidia Jetson TX1 to run ML models prepared with Amazon SageMaker.

## Get started

1. Create an S3 bucket to host the models.

1. Create a lambda with the Python2.7 runtime, create an alias "latest" pointing to $LATEST.

1. `python3 create-greengrass-config.py --create-group GG-ML-Workshop --bucket my-greengrass-models --function demo-inference`

    - Change the 3 parameters to values of your choice (Group Name, Bucket Name and Function Name)

1. Upload the resulting **certificates.tar.gz** on your device.

1. Go back to the console and hit Deploy in your Greengrass Group.

1. Wait for a short while, and run `python3 create-greengrass-config.py --ip-address` to get the IP of your device.

You're now set to start doing some ML @Edge.

## A first model running on Greengrass

1. Go in the first directory 01-face-detection.

1. Edit Makefile.parameters with your values.

## Tips

### mplayer from remote computer to view the lambda's output

`ssh DEVICE cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32`

### mplayer on framebuffer to view the lambda's output

`ssh DEVICE DISPLAY=0:0 mplayer /tmp/results.mjpeg -vo fbdev -demuxer lavf -lavfdopts format=mjpeg:probesize=32 -fs -zoom -xy 1280`