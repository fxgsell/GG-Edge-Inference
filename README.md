# GG-Edge-Inference

Using AWS Greengrass with the Nvidia Jetson TX1 to run ML models prepared with Amazon SageMaker.


# Tips

### View Camera

gst-launch-1.0 nvcamerasrc sensor-id=0 ! 'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1, format=NV12' ! nvoverlaysink -ev

### mplayer to view the lambda's output

mplayer –demuxer lavf -lavfdopts format=mjpeg:probesize=32 /tmp/ssd_results.mjpeg

### Remote mplayer

ssh benny cat /tmp/results.mjpeg | mplayer - -demuxer lavf -lavfdopts format=mjpeg:probesize=32 
