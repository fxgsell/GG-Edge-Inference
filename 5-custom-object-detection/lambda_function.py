import os
import cv2
import time
from threading import Timer

from file_output import FileOutput
from publish import Publisher
from inference import Infer
from camera import VideoStream

IOT_TOPIC = 'custom_object_detection/inference'
IOT_TOPIC_ADMIN = 'custom_object_detection/admin'

def get_parameter(name, default):
    if name in os.environ and os.environ[name] != "":
        return os.environ[name]
    return default

THING_NAME = get_parameter('AWS_IOT_THING_NAME', "Unknown")

PUB = Publisher(IOT_TOPIC_ADMIN, IOT_TOPIC, THING_NAME)

PUB.info("Loading new Thread")
PUB.info('OpenCV '+cv2.__version__)

def lambda_handler(event, context):
    return

try:
    VS = VideoStream().start()
except Exception as err:
    PUB.exception(str(err))
PUB.info('Camera is ' + VS.device)

font = cv2.FONT_HERSHEY_DUPLEX
frame = VS.read()
cv2.putText(frame, 'Loading...', (0, 30), font, 1.0, (0, 0, 0), lineType=cv2.LINE_AA) 

OUTPUT = FileOutput('/tmp/results.mjpeg', frame, PUB)
OUTPUT.start()

model = Infer()

def main_loop():
    try:
        last_update = time.time()
        results = []
        last_fps, fps = 0, 0

        while 42 :
            frame = VS.read()
            try:
                dets = model.do(frame)
                detected = model.visualize(dets, frame)
                results += detected
            except Exception as err:
                PUB.exception(str(err))
                raise err
            
            fps += 1
            now = time.time()
            if now - last_update >= 1:
                last_update = time.time()
                PUB.events(results)
                last_fps = fps
                fps = 0
                results = []
            cv2.putText(frame, str(last_fps) + 'fps', (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA) 
            OUTPUT.update(frame)

    except Exception as err:
        PUB.exception(str(err))

    Timer(1, main_loop).start()

main_loop()
