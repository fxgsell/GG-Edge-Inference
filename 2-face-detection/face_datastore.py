import numpy as np

class FaceDatastore:
    def __init__(self, count=6):
        ''' Constructor '''
        self.face_encodings = []
        self.face_names = []
        self.tolerance = 0.6
        self.seen = 0
        self.max_length = count

    def is_known(self, face):
        norm = np.empty((0))
        best = 1
        if self.face_encodings:
            norm = np.linalg.norm(self.face_encodings - face, axis=1)
            best = norm.min()
 
        if best <= self.tolerance:
            i = np.where(norm == best)
            name = self.face_names[i[0][0]]
        else:
            if len(self.face_encodings) >= self.max_length:
                self.face_encodings.pop(0)
                self.face_names.pop(0)

            name = "New"+str(self.seen)
            self.seen += 1

            self.face_encodings.append(face)
            self.face_names.append(name)
        return name
