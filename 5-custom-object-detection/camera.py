'''
Module camera provides the VideoStream class which
offers a threaded interface to multiple types of cameras.
'''
from threading import Thread
import os
import platform
import cv2 # pylint: disable=import-error

DEEPLENS = True
try:
    import awscam
except ImportError:
    DEEPLENS = False

class VideoStream:
    '''
    Instantiate the VideStream class and call the start() method
    to be able to read from the camera, instantiate only once.
    Use the method read() to get the latest frame.
    '''
    def __init__(self):
        ''' Constructor. Chooses a camera to read from. '''
        self.width = 640
        self.height = 480
        self.device = '/dev/video1'

        if DEEPLENS:
            True
        elif platform.system() == 'Darwin':
            self.device = 'Webcam'
            self.stream = cv2.VideoCapture(0)
            self.stream.set(3,self.width)
            self.stream.set(4,self.height)
        elif os.path.isfile('/dev/video1'):
            self.device = '/dev/video1'
            self.stream = cv2.VideoCapture('/dev/video1')
        elif os.path.isfile('/dev/video0'):
            self.device = '/dev/video0'
            self.stream = cv2.VideoCapture('/dev/video0')
        else:
            self.device = 'GStreamer'
            HD_2K = False
            if HD_2K:
                self.width = 2592  #648
                self.height = 1944 #486
            else:
                self.width = 1296  #324
                self.height = 972  #243
            
            gst_str = ("nvcamerasrc ! "
                    "video/x-raw(memory:NVMM), width=(int)2592, height=(int)1944,"
                    "format=(string)I420, framerate=(fraction)30/1 ! "
                    "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, "
                    "format=(string)BGRx ! videoconvert ! appsink").format(self.width, self.height)
            self.stream = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
        self.stopped = False

        if not self.stream.isOpened():
            raise Exception("Failed to open camera.")

        _, self.frame = self.stream.read()

    def get_height(self):
        return self.height

    def get_width(self):
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
        if DEEPLENS:
            ret, self.frame = awscam.getLastFrame()
        return self.frame

    def stop(self):
        '''stop() set a flag to stop the update loop'''
        self.stopped = True
