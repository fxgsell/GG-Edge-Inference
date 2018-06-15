import mxnet as mx
import cv2
import numpy as np
from collections import namedtuple

# to run locally
# from inference import Infer  # from python prompt

class Infer:
    Batch = namedtuple('Batch', ['data'])

    def __init__(self, path="/ml/boxes/image-classification"): ## TODO: Update the path
        self.categories = ['bad', 'good', 'none']

        self.data_shape = 227
        sym, args, auxs = mx.model.load_checkpoint(path, 10)
        self.mod = mx.mod.Module(sym, label_names=None, context=mx.gpu())
        self.mod.bind(data_shapes=[('data', (1, 3, 227, 227))], label_shapes=self.mod._label_shapes)
        self.mod.set_params(args, auxs, allow_missing=True)

    def do(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.swapaxes(frame, 0, 2)
        frame = np.swapaxes(frame, 1, 2)
        frame = frame[np.newaxis, :]
        self.mod.forward(self.Batch([mx.nd.array(frame)]))
        dets = self.mod.get_outputs()[0].asnumpy()[0]
        print(dets) #debug
        category = np.argmax(dets)
        return self.categories[category]