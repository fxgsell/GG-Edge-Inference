import numpy as np

class FaceDatastore:
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.tolerance = 0.6
        self.seen = 0

    def is_known(self, face):
        norm = np.empty((0))
        if len(self.face_encodings) > 0:
            norm = np.linalg.norm(self.face_encodings - face, axis=1)
        matches = list(norm <= self.tolerance)

        # If a match was found in face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = self.face_names[first_match_index]
        else:
            if len(self.face_encodings) >= 6:
                self.face_encodings.pop(0)
                self.face_names.pop(0) 

            name = "New"+str(self.seen)
            self.seen += 1

            self.face_encodings.append(face)
            self.face_names.append(name)

            return name
