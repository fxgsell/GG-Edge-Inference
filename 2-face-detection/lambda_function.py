import os
import platform
import face_recognition
import json
import cv2 # pylint: disable=import-error
from camera import VideoStream
from file_output import FileOutput
from face_datastore import FaceDatastore
from publish import Publisher

IOT_TOPIC = 'jetson/inference'
IOT_TOPIC_ADMIN = 'jetson/admin'

THING_NAME = "Unknown"
if "THING_NAME" in os.environ and os.environ['THING_NAME'] != "":
    THING_NAME = os.environ['THING_NAME']

FULL_SIZE = True
if "FULL_SIZE" in os.environ and os.environ['FULL_SIZE'] == "0":
    FULL_SIZE = False

PUB = Publisher(IOT_TOPIC_ADMIN, IOT_TOPIC)

PUB.publish(topic=IOT_TOPIC_ADMIN, payload=json.dumps({
    "type":  "info",
    "payload": "Loading new Thread"
}))
PUB.publish(topic=IOT_TOPIC_ADMIN, payload=json.dumps({
    "type":  "info",
    "payload": 'OpenCV '+cv2.__version__
}))

def draw_box(frame, name, top, right, bottom, left):
    ''' Draw a box with a label. '''
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame

def main_loop():
    try:
        VS = VideoStream().start()
    except Exception as err:
        PUB.publish(topic=IOT_TOPIC_ADMIN, payload=json.dumps({
            "type":  "exception",
            "location": "VideoStream",
            "line": 63,
            "payload": str(err)
        }))
        
    OUTPUT = FileOutput('/tmp/results.mjpeg', VS.read(), PUB)
    OUTPUT.start()

    try:
        FACES = FaceDatastore()
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
                    name = FACES.is_known(face_encoding)
                except Exception as err:
                    PUB.publish(topic=IOT_TOPIC_ADMIN, payload=json.dumps({
                        "type":  "exception",
                        "location": "is_known",
                        "line": 63,
                        "payload": str(err)
                    }))
                    raise err

                names.append(name)

                if not FULL_SIZE:
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                frame = draw_box(frame, name, top, right, bottom, left)

            if names:
                PUB.publish(topic=IOT_TOPIC, payload=json.dumps({
                    "type":  "event",
                    "payload": names
                }))

            OUTPUT.update(frame)

    except Exception as err:
        PUB.publish(topic=IOT_TOPIC_ADMIN, payload=json.dumps({
            "type":  "exception",
            "location": "main_loop",
            "line": 87,
            "payload": str(err)
        }))

    OUTPUT.stop()
    VS.stop()

main_loop()

def lambda_handler(event, context):
    return
