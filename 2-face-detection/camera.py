'''
Module camera provides the VideoStream class which
offers a threaded interface to multiple types of cameras.
'''
from threading import Thread
import os
import platform
import cv2 # pylint: disable=import-error

class VideoStream:
    '''
    Instantiate the VideStream class and call the start() method
    to be able to read from the camera, instantiate only once.
    Use the method read() to get the latest frame.
    '''
    def __init__(self):
        ''' Constructor. Chooses a camera to read from. '''
        if platform.system() == 'Darwin':
            self.stream = cv2.VideoCapture(0)
            self.stream.set(3,640)
            self.stream.set(4,480)
        elif os.path.isfile('/dev/video1'):
            self.stream = cv2.VideoCapture('/dev/video1')
        elif os.path.isfile('/dev/video0'):
            self.stream = cv2.VideoCapture('/dev/video0')
        else:
            width = 640
            height = 480
            gst_str = ("nvcamerasrc ! "
                    "video/x-raw(memory:NVMM), width=(int)2592, height=(int)1458,"
                    "format=(string)I420, framerate=(fraction)30/1 ! "
                    "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, "
                    "format=(string)BGRx ! videoconvert ! appsink").format(width, height)
            self.stream = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
        self.stopped = False

        if not self.stream.isOpened():
            raise Exception("Failed to open camera.")

        _, self.frame = self.stream.read()

    def height(self):
        return self.height

    def width(self):
        return self.width

    def start(self):
        '''start() starts the thread'''
        thread = Thread(target=self.update, args=())
        thread.daemon = True
        thread.start()
        return self

    def update(self):
        '''update() constantly read the camera stream'''
        while not self.stopped:
            _, self.frame = self.stream.read()

    def read(self):
        '''read() return the last frame captured'''
        return self.frame

    def stop(self):
        '''stop() set a flag to stop the update loop'''
        self.stopped = True
