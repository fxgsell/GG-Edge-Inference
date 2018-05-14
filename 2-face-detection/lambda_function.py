from timeit import default_timer as timer
from threading import Timer
from collections import namedtuple
from threading import Thread
import time
import os
import greengrasssdk
import face_recognition
import random
import cv2
import json
import numpy as np
import sys

Batch = namedtuple('Batch', ['data'])

IOT_TOPIC = 'jetson/inference'
IOT_TOPIC_ADMIN = 'jetson/admin'

GGC = greengrasssdk.client('iot-data')
THING_NAME="Jetson-3_Core"
FILE_OUTPUT = True

def random_color():
    rgbl=[255,0,0]
    random.shuffle(rgbl)
    return tuple(rgbl)

class FileVideoStream:
    def __init__(self, device):
        def open_cam_onboard(width, height):
            gst_str = ("nvcamerasrc ! "
                        "video/x-raw(memory:NVMM), width=(int)2592, height=(int)1458, format=(string)I420, framerate=(fraction)30/1 ! "
                        "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
                        "videoconvert ! appsink").format(width, height)
            return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

        self.stream = open_cam_onboard(640, 480)

        
        self.stopped = False

        if not self.stream.isOpened():
            GGC.publish(topic=IOT_TOPIC_ADMIN, payload="Failed to open camera!")
            sys.exit("Failed to open camera!")
        else:
            print("Cam is opened")

        self.grabbed, self.frame = self.stream.read()

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self   

    def update(self):
        while True:
            if self.stopped:
                return

            self.grabbed, self.frame = self.stream.read()

    def read(self):
    	return self.frame

    def stop(self):
	    self.stopped = True

fvs = FileVideoStream(1).start()
frame = fvs.read()
time.sleep(2)
frame = fvs.read()
_, jpeg = cv2.imencode('.jpg', frame)

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
                GGC.publish(topic=IOT_TOPIC_ADMIN, payload=e)
                continue

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []
seen = 0

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

colors = [
    (255 , 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

GGC.publish(topic=IOT_TOPIC_ADMIN, payload='Loading new Thread.')
GGC.publish(topic=IOT_TOPIC_ADMIN, payload='CV: '+cv2.__version__)

def is_known(face):
    tolerance = 0.6
    norm = np.empty((0))
    try:
        if len(known_face_encodings) > 0:
            norm = np.linalg.norm(known_face_encodings - face, axis=1)
    except Exception as e:
        msg = "Matching faces: " + str(e)
        GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)
        raise e

    return list(norm <= tolerance)

def loop():
    try:
        start = timer()
        last_face = ""
        if FILE_OUTPUT:
            results_thread = FIFO_Thread()
            results_thread.start()

        ### inference
        while 42:
            frame = fvs.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                matches = is_known(face_encoding)
                name = ""

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                else:
                    if len(known_face_encodings) >= 6:
                        known_face_encodings.pop(0)
                        known_face_names.pop(0) 
                    
                    global seen
                    name = "User"+str(seen)
                    seen = seen + 1

                    known_face_encodings.append(face_encoding)
                    known_face_names.append(name)

                face_names.append(name)

                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                time_start = timer() - start
                if name != last_face and time_start >= 5:
                    last_face = name
                    GGC.publish(topic=IOT_TOPIC, payload=name)

                # time_matching = timer() - start
                # msg = "Matching time: {:.4f} sec".format(time_matching)
                # GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)

            if FILE_OUTPUT:
                global jpeg
                _, jpeg = cv2.imencode('.jpg', frame)

            # time_frame = timer() - start
            # msg = "Total time: {:.4f} sec".format(time_frame)
            # GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)
        

    except Exception as e:
        msg = "Test failed: " + str(e)
        GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)

loop()

def lambda_handler(event, context):
    return
