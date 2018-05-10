import argparse
from symbol.symbol_factory import get_symbol
import numpy as np
from timeit import default_timer as timer
from threading import Timer
import cv2
from collections import namedtuple
from threading import Thread
import time
import random
import os
import greengrasssdk
import mxnet as mx
import platform

Batch = namedtuple('Batch', ['data'])

VERSION = "7"
THRESHOLD = 0.6
IOT_TOPIC = 'jetson/inference'
IOT_TOPIC_ADMIN = 'jetson/admin'
DATA_SHAPE = 512

GGC = greengrasssdk.client('iot-data')
PLATFORM = platform.platform()

FILE_OUTPUT = True

GGC.publish(topic=IOT_TOPIC_ADMIN, payload='Loading new Thread.')
GGC.publish(topic=IOT_TOPIC_ADMIN, payload='Platfom: '+PLATFORM)
GGC.publish(topic=IOT_TOPIC_ADMIN, payload='MXNet: '+mx.__version__)
GGC.publish(topic=IOT_TOPIC_ADMIN, payload='CV: '+cv2.__version__)

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
            print("Failed to open camera!")
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

fvs = FileVideoStream(0).start()
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
        GGC.publish(topic=IOT_TOPIC_ADMIN, payload="Opened Output Pipe")
        while Write_To_FIFO:
            try:
                f.write(jpeg.tobytes())
            except IOError as e:
                print(e)
                continue

def draw_box(frame, corners, color, label, proba):
    def bright(color):
        r, g, b = color
        if (r*299 + g*587 + b*114) / 1000 > 128:
            return True
        return False

    height = DATA_SHAPE
    width = DATA_SHAPE
    xmin = int(corners[0] * width)
    ymin = int(corners[1] * height)
    xmax = int(corners[2] * width)
    ymax = int(corners[3] * height)
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
    
    txt_color = (255, 255, 255)
    if bright(color):
        txt_color = (0, 0, 0)

    y_txt = 10
    ymin = ymin - y_txt if ymin - y_txt >= 0 else 0
    xmin = xmin - 1
    xmax = xmax + 1
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymin + y_txt), color, -1)
    cv2.putText(frame, label + ' ' + str(round(proba, 2)) + '%', (xmin, ymin+y_txt), cv2.FONT_HERSHEY_DUPLEX, 0.4, txt_color)

    return frame


colors = {}

def loop():
    EPOCH = 0
    BATCH_SIZE = 1
    prefix = '/trained_models/resnet/ssd_resnet50_512'
    network = 'resnet50'
    classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 
                'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
                'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

    try:
        ctx = mx.gpu(0)
        symbol = get_symbol(network, DATA_SHAPE, num_classes=len(classes), nms_thresh=0.5, \
            force_nms=True, nms_topk=400)

        ### init model
        load_symbol, args, auxs = mx.model.load_checkpoint(prefix, EPOCH)
        if symbol is None:
            symbol = load_symbol
        mod = mx.mod.Module(symbol, label_names=None, context=ctx)
        mod.bind(data_shapes=[('data', (BATCH_SIZE, 3, DATA_SHAPE, DATA_SHAPE))])
        mod.set_params(args, auxs)

        if FILE_OUTPUT:
            results_thread = FIFO_Thread()
            results_thread.start()

        ### inference
        while 42:
            img = fvs.read()
            img = cv2.resize(img, (DATA_SHAPE, DATA_SHAPE))

            frame = img
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = np.swapaxes(img, 0, 2)
            img = np.swapaxes(img, 1, 2)
            img = img[np.newaxis, :]

            start = timer()
            mod.forward(Batch([mx.nd.array(img)]))
            dets = mod.get_outputs()[0].asnumpy()[0]
            for i in dets[np.where(dets[:, 0] >= 0)]:
                proba = i[1]
                if proba >= THRESHOLD:
                    cls_id = classes[int(i[0])]
                    msg = "Class: " + cls_id + ", Proba: " + str(i[1]) + "%"
                    GGC.publish(topic=IOT_TOPIC, payload=msg)
                    print(msg)
                    if cls_id not in colors:
                        colors[cls_id] = random_color()
                    frame = draw_box(frame, i[2:], colors[cls_id], cls_id, proba)

            if FILE_OUTPUT:
                global jpeg
                _, jpeg = cv2.imencode('.jpg', frame)

            time_elapsed = timer() - start
            print("Detection time: {:.4f} sec".format(time_elapsed))
            

    except Exception as e:
        msg = "Test failed: " + str(e)
        print(msg)
        GGC.publish(topic=IOT_TOPIC_ADMIN, payload=msg)

    Timer(15, loop).start()

loop()

def lambda_handler(event, context):
    return
