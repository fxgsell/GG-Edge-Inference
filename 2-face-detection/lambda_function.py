from threading import Thread
import greengrasssdk
import face_recognition
import cv2 # pylint: disable=import-error
from camera import VideoStream
from file_output import FileOutput
from face_datastore import FaceDatastore
import os

IOT_TOPIC = 'jetson/inference'
IOT_TOPIC_ADMIN = 'jetson/admin'

GGC = greengrasssdk.client('iot-data')
THING_NAME="Jetson-3_Core"
FILE_OUTPUT = True
FULL_SIZE = True

if "DEVICE" in os.environ and os.environ['DEVICE'] == "PI":
    FULL_SIZE = False

try:
    vs = VideoStream().start()
except Exception as e:
    msg = "Exiting: (VideoStream:__init__) " + str(e)
    GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)
    exit(msg)

GGC.publish(topic=IOT_TOPIC_ADMIN, payload='Info: Loading new Thread.')
GGC.publish(topic=IOT_TOPIC_ADMIN, payload='Info: OpenCV '+cv2.__version__)

def draw_box(frame, name, top, right, bottom, left):
    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame


def main_loop():
    if FILE_OUTPUT:
        results = FileOutput('/tmp/results.mjpeg', vs.read())
        results.start()

    ### inference
    try:
        while 42:
            frame = vs.read()
            faces = FaceDatastore()

            if FULL_SIZE:
                rgb_frame = frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            else:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                try:
                    name = faces.is_known(face_encoding)
                except Exception as e:
                    msg = "Exception: (is_known) "+ str(e)
                    GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)
                    raise e

                face_names.append(name)

                if not FULL_SIZE:
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                frame = draw_box(frame, name, top, right, bottom, left)

            msg = "Info: (main_loop) Face(s) detected: " + str(face_names)
            GGC.publish(topic=IOT_TOPIC, payload=msg)

            if FILE_OUTPUT:
                results.update(frame)

    except Exception as e:
        msg = "Exception: (main_loop) "+ str(e)
        GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)

    if FILE_OUTPUT:
        results.stop()

    vs.stop()

main_loop()

def lambda_handler(event, context):
    return
