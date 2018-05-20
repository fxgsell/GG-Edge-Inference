from threading import Thread
import os
import json
import cv2 # pylint: disable=import-error

class FileOutput(Thread):
    '''
    File output manage an opencv frame output
    saving it to disque in mjpeg format.
    '''
    def __init__(self, path, frame, publisher):
        ''' Constructor. '''
        Thread.__init__(self)

        self.stopped = False
        self.path = path
        self.update(frame)
        self.publisher = publisher

    def stop(self):
        '''stop() set a flag to stop the run loop'''
        self.stopped = True

    def update(self, frame):
        '''update() refresh the last opencv frame'''
        _, jpeg = cv2.imencode('.jpg', frame)
        self.jpeg = jpeg

    def run(self):
        '''update() constantly update the file on drive'''
        if not os.path.exists(self.path):
            os.mkfifo(self.path)
        file = open(self.path, 'w')
        while not self.stopped:
            try:
                file.write(self.jpeg.tobytes())
            except IOError as err:
                self.publisher.exception(str(err))
                file = open(self.path, 'w')
                continue
