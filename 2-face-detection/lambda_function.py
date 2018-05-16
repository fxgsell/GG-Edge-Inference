from threading import Thread
import greengrasssdk
import face_recognition
import cv2
import numpy as np
from camera import VideoStream
from file_output import FileOutput

IOT_TOPIC = 'jetson/inference'
IOT_TOPIC_ADMIN = 'jetson/admin'

GGC = greengrasssdk.client('iot-data')
THING_NAME="Jetson-3_Core"
FILE_OUTPUT = True
FULL_SIZE = False

try:
    fvs = VideoStream('/dev/video0').start()
except Exception as e:
    msg = "Exiting: (FileVideoStream:__init__) " + str(e)
    GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)
    exit(msg)

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []
seen = 0

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

GGC.publish(topic=IOT_TOPIC_ADMIN, payload='Info: Loading new Thread.')
GGC.publish(topic=IOT_TOPIC_ADMIN, payload='Info: OpenCV '+cv2.__version__)

def is_known(face):
    tolerance = 0.6
    norm = np.empty((0))
    try:
        if len(known_face_encodings) > 0:
            norm = np.linalg.norm(known_face_encodings - face, axis=1)
    except Exception as e:
        msg = "Exception: (is_known) "+ str(e)
        GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)
        raise e
    return list(norm <= tolerance)

def main_loop():
    if FILE_OUTPUT:
        results = FileOutput('/tmp/results.mjpeg', fvs.read())
        results.start()

    ### inference
    try:
        while 42:
            frame = fvs.read()

            if FULL_SIZE:
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)
            else:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
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
                    name = "New"+str(seen)
                    seen = seen + 1

                    known_face_encodings.append(face_encoding)
                    known_face_names.append(name)

                    msg = "Info: (main_loop) New face detected: " + name
                    GGC.publish(topic=IOT_TOPIC, payload=msg)

                face_names.append(name)

                if not FULL_SIZE:
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

            if FILE_OUTPUT:
                results.update(frame)

    except Exception as e:
        msg = "Exception: (main_loop) "+ str(e)
        GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)

    if FILE_OUTPUT:
        results.stop()

    fvs.stop()

main_loop()

def lambda_handler(event, context):
    return
