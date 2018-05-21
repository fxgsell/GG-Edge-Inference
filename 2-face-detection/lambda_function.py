import os
import platform
import face_recognition
import json
import cv2
import base64
from threading import Timer
import uuid

from camera import VideoStream
from file_output import FileOutput
from face_datastore import FaceDatastore
from publish import Publisher

IOT_TOPIC = 'jetson/inference'
IOT_TOPIC_ADMIN = 'jetson/admin'

def get_parameter(name, default):
    if name in os.environ and os.environ[name] != "":
        return os.environ[name]
    return default

THING_NAME = get_parameter('THING_NAME', "Unknown")

FULL_SIZE = get_parameter('FULL_SIZE', '1')
FULL_SIZE = True if FULL_SIZE == '1' else False

PUB = Publisher(IOT_TOPIC_ADMIN, IOT_TOPIC, THING_NAME)

PUB.info("Loading new Thread")
PUB.info('OpenCV '+cv2.__version__)

FACES = FaceDatastore()

def lambda_handler(event, context):
    PUB.info("Received update: " + json.dumps(event))
    for key  in  event:
        FACES.update_face(key, event[key])
    return

def draw_box(frame, name, top, right, bottom, left):
    ''' Draw a box with a label. '''
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame

try:
    VS = VideoStream().start()
except Exception as err:
    PUB.exception(str(err))

OUTPUT = FileOutput('/tmp/results.mjpeg', VS.read(), PUB)
OUTPUT.start()

def main_loop():
    try:
        frame = VS.read()

        if FULL_SIZE:
            rgb_frame = frame[:, :, ::-1]
        else:
            rgb_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        names = []
        known = True
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            try:
                name, known = FACES.is_known(face_encoding)
            except Exception as err:
                PUB.exception(str(err))
                raise err

            names.append(name)

            if not FULL_SIZE:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

            if not known and bottom-top > 40:
                face = frame[max(top - top, 0):min(bottom + bottom, VS.height()),
                                max(left - left, 0):min(right + right, VS.width())]
                _, jpeg = cv2.imencode('.jpg', face)
                PUB.publish(
                    topic="face_recognition/new",
                    payload={
                        'id': name,
                        'uuid': str(uuid.uuid1()),
                        'face': base64.b64encode(jpeg.tobytes())
                    })

            frame = draw_box(frame, name, top, right, bottom, left)

        PUB.events(names)
        OUTPUT.update(frame)

    except Exception as err:
        PUB.exception(str(err))

    Timer(0, main_loop).start()

# OUTPUT.stop()
# VS.stop()

main_loop()
