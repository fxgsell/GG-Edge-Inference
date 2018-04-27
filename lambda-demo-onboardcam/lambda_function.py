from threading import Timer
from threading import Thread
import os
import time
import sys
import cv2

def open_cam_onboard(width, height):
    gst_str = ("nvcamerasrc ! "
                "video/x-raw(memory:NVMM), width=(int)2592, height=(int)1458, format=(string)I420, framerate=(fraction)30/1 ! "
                "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
                "videoconvert ! appsink").format(width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

cap = open_cam_onboard(640, 480)

time.sleep(2)

if not cap.isOpened():
    sys.exit("Failed to open camera!")
else:
    print("Cam is opened")

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
        while Write_To_FIFO:
            try:
                f.write(jpeg.tobytes())
            except IOError as e:
                continue


def inf_loop():
    global Write_To_FIFO
    Write_To_FIFO = True
    try:
        results_thread = FIFO_Thread()
        results_thread.start()
        while True:
            _, frame = cap.read()
            global jpeg
            _, jpeg = cv2.imencode('.jpg', frame)
    except Exception as e:
        msg = "Model loading error bis: " + str(e)
        print(msg)
   
    Write_To_FIFO = False
    #Timer(15, inf_loop).start()

inf_loop()
# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return