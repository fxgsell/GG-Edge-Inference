# This can be found on the AWS IoT Console.
import io
import sys
import os
import logging
import platform
from threading import Timer
from threading import Thread
from time import sleep

import greengrasssdk
import cv2
import load_model

VERSION = "6"
THRESHOLD = 0.3
IOT_TOPIC = 'inference/demo'

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

GGC = greengrasssdk.client('iot-data')
PLATFORM = platform.platform()
MODEL_PATH = '/trained_model/squeezenet/'
SYNSET_PATH = MODEL_PATH + 'synset.txt'
NETWORK_PATH = MODEL_PATH + 'squeezenet_v1.1'

def open_cam_usb(dev):
    return cv2.VideoCapture(dev)

cap = open_cam_usb(1)

if not cap.isOpened():
    GGC.publish(topic=IOT_TOPIC, payload='Error failed to open camera')
    sys.exit("Failed to open camera!")
else:
    GGC.publish(topic=IOT_TOPIC, payload='Initilized camera successfully')

ret, frame = cap.read()
ret, jpeg = cv2.imencode('.jpg', frame)
Write_To_FIFO = True
class FIFO_Thread(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

    def run(self):
        fifo_path = "/tmp/results.mjpeg"
        if not os.path.exists(fifo_path):
            os.mkfifo(fifo_path)
        f = open(fifo_path, 'w')
        GGC.publish(topic=IOT_TOPIC, payload="Opened Pipe")
        while Write_To_FIFO:
            try:
                f.write(jpeg.tobytes())
            except IOError as e:
                continue

def inf_loop():
    try:
        global_model = load_model.ImagenetModel(SYNSET_PATH, NETWORK_PATH)
        GGC.publish(topic=IOT_TOPIC, payload=str("Initilized model"))
        results_thread = FIFO_Thread()
        results_thread.start()
        while True:
            # Get the last frame
            ret, frame = cap.read()

            # Send fram to model
            predictions = global_model.predict_from_image(frame)

            # Send predictions to IOT
            #GGC.publish(topic=IOT_TOPIC, payload=str(predictions))

            # Update the output for mplayer
            global jpeg
            ret, jpeg = cv2.imencode('.jpg', frame)

    except Exception as e:
        msg = "Test failed: " + str(e)
        GGC.publish(topic=IOT_TOPIC, payload=msg)

    Timer(15, inf_loop).start()

inf_loop()

def lambda_handler(event, context):
    return
