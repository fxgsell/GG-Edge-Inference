import numpy as np
import time

TIMEOUT = 60

class FaceDatastore:
    def __init__(self, count=6, tolerance=0.6):
        ''' Constructor '''
        self.face_encodings = []
        self.face_id = []
        self.face_time = []
        self.face_names = []
        self.tolerance = tolerance
        self.max_length = count
        self.seen = 0

    def update_face(self, old, new):
        for i, v in enumerate(self.face_names):
            if v == old:
                self.face_names[i] = new

    def is_known(self, face):
        norm = np.empty((0))
        best = 1
        if self.face_encodings:
            norm = np.linalg.norm(self.face_encodings - face, axis=1)
            best = norm.min()

        if best <= self.tolerance:
            id = np.where(norm == best)[0][0]
            name = self.face_names[id]

            if self.face_id[id] != name:
                return name, True
            elif (self.face_time[id] + TIMEOUT) > int(time.time()):
                return name, True
            self.face_time[id] = int(time.time())
        else:
            if len(self.face_encodings) >= self.max_length:
                self.face_encodings.pop(0)
                self.face_names.pop(0)
                self.face_id.pop(0)
                self.face_time.pop(0)

            name = "New"+str(self.seen)
            self.seen += 1

            self.face_encodings.append(face)
            self.face_id.append(name)
            self.face_names.append(name)
            self.face_time.append(int(time.time()))
        return name, False
