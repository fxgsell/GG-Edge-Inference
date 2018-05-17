import os
import platform
import face_recognition
import cv2 # pylint: disable=import-error
from camera import VideoStream
from file_output import FileOutput
from face_datastore import FaceDatastore
from publish import publish

IOT_TOPIC = 'jetson/inference'
IOT_TOPIC_ADMIN = 'jetson/admin'

THING_NAME = "Jetson-3_Core"
FILE_OUTPUT = True
FULL_SIZE = True

if "DEVICE" in os.environ and os.environ['DEVICE'] == "PI":
    FULL_SIZE = False

try:
    VS = VideoStream().start()
except Exception as err:
    MSG = "Exiting: (VideoStream:__init__) " + str(err)
    publish(topic=IOT_TOPIC_ADMIN, payload=MSG)
    exit(MSG)

publish(topic=IOT_TOPIC_ADMIN, payload='Info: Loading new Thread.')
publish(topic=IOT_TOPIC_ADMIN, payload='Info: OpenCV '+cv2.__version__)

def draw_box(frame, name, top, right, bottom, left):
    ''' Draw a box with a label. '''
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame

def main_loop():
    if FILE_OUTPUT:
        results = FileOutput('/tmp/results.mjpeg', VS.read())
        results.start()

    ### inference
    try:
        faces = FaceDatastore()
        while 42:
            frame = VS.read()

            if FULL_SIZE:
                rgb_frame = frame[:, :, ::-1]
            else:
                rgb_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            names = []

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                try:
                    name = faces.is_known(face_encoding)
                except Exception as err:
                    msg = "Exception: (is_known) "+ str(err)
                    publish(topic=IOT_TOPIC_ADMIN, payload=msg)
                    print(err)
                    raise err

                names.append(name)

                if not FULL_SIZE:
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                frame = draw_box(frame, name, top, right, bottom, left)

            msg = "Info: (main_loop) Face(s) detected: " + str(names)
            publish(topic=IOT_TOPIC, payload=msg)

            if FILE_OUTPUT:
                results.update(frame)

    except Exception as err:
        msg = "Exception: (main_loop) "+ str(err)
        publish(topic=IOT_TOPIC_ADMIN, payload=msg)

    if FILE_OUTPUT:
        results.stop()

    VS.stop()

main_loop()

def lambda_handler(event, context):
    return
