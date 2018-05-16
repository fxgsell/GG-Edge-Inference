from threading import Thread
import os
import cv2

class VideoStream:
    def __init__(self, device):
        def open_cam_onboard(width, height):
            gst_str = ("nvcamerasrc ! "
                        "video/x-raw(memory:NVMM), width=(int)2592, height=(int)1458, format=(string)I420, framerate=(fraction)30/1 ! "
                        "nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! "
                        "videoconvert ! appsink").format(width, height)
            return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

        if os.path.isfile(device):
            self.stream = cv2.VideoCapture(device)
        else:
            self.stream = open_cam_onboard(640, 480)

        self.stopped = False

        if not self.stream.isOpened():
            raise "Failed to open camera."

        _, self.frame = self.stream.read()

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self   

    def update(self):
        while not self.stopped:
            _, self.frame = self.stream.read()

    def read(self):
    	return self.frame

    def stop(self):
	    self.stopped = True