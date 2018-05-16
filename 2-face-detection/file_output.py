from threading import Thread
import os
import cv2

class FileOutput(Thread):
    def __init__(self, path, frame):
        ''' Constructor. '''
        Thread.__init__(self)

        self.stopped = False
        self.path = path
        self.update(frame)

    def stop(self):
        self.stopped = True

    def update(self, frame):
        _, jpeg = cv2.imencode('.jpg', frame)
        self.jpeg = jpeg

    def run(self):
        if not os.path.exists(self.path):
            os.mkfifo(self.path)
        f = open(self.path, 'w')
        while not self.stopped:
            try:
                f.write(self.jpeg.tobytes())
            except IOError as e:
                print("Exception: (FileOutput:run) "+ str(e))
                f = open(self.path, 'w')
                continue