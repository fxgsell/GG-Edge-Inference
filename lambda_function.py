# This can be found on the AWS IoT Console.
import io
import cv2
import load_model
import numpy as np
import sys
import os
import logging
import platform
import greengrasssdk

from threading import Timer
from time import sleep

VERSION = "6"
THRESHOLD = 0.3

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

GGC = greengrasssdk.client('iot-data')
PLATFORM = platform.platform()

def open_cam_usb(dev):
    return cv2.VideoCapture(dev)

cap = open_cam_usb(1)

if not cap.isOpened():
    GGC.publish(topic='hello/world', payload='Error failed to open camera')
    sys.exit("Failed to open camera!")
else:
    GGC.publish(topic='hello/world', payload='Initilized camera successfully')

#model_path = '/greengrass-machine-learning/mxnet/squeezenet/'
model_path = './'
global_model = load_model.ImagenetModel(model_path + 'synset.txt', model_path + 'squeezenet_v1.1')

i = 0
GGC.publish(topic='hello/world', payload=str("Initilized model"))

def clean_predictions(predictions):
    validated = []

    for k, v in predictions:
        if k > THRESHOLD:
            validated.append({'Object': v, 'Percentage': k})
    return validated

last_prediction = ""
while True:
    ret, frame = cap.read()
    print(ret)

    predictions = global_model.predict_from_image(frame)
    GGC.publish(topic='hello/world', payload=str(predictions))
    sleep(1)

def lambda_handler(event, context):
    return

