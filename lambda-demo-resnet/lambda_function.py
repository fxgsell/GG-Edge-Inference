import os
import greengrasssdk
from threading import Timer
import time
import cv2
from threading import Thread
import base64
import load_model
import sys

# Creating a greengrass core sdk client
GGC = greengrasssdk.client('iot-data')
IOT_TOPIC = 'inference/resnet'
MODEL_PATH = '/trained_model/ssd_resnet50_512/'
NETWORK_PATH = MODEL_PATH + 'ssd_resnet50_512'
SYNSET_PATH = MODEL_PATH + 'synset.txt'

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
        #results_thread = FIFO_Thread()
        #results_thread.start()
        try:
            while True:
                ret, frame = cap.read()
                predictions = global_model.predict_from_image(frame)
                GGC.publish(topic=IOT_TOPIC, payload=str(predictions))
                #global jpeg
                #ret, jpeg = cv2.imencode('.jpg', frame)
                time.sleep(1)

        except Exception as e:
            msg = "Inference error: " + str(e)
            GGC.publish(topic=IOT_TOPIC, payload=msg)

    except Exception as e:
        msg = "Model loading error bis: " + str(e)
        GGC.publish(topic=IOT_TOPIC, payload=msg)
   

    Timer(15, inf_loop).start()

inf_loop()
# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return