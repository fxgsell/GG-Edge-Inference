import mxnet as mx
import cv2
import numpy as np
from collections import namedtuple
from symbol.symbol_factory import get_symbol
import random

# to run locally
# from inference import Infer  # from python prompt

def gpu_device(gpu_number=0):
    try:
        _ = mx.nd.array([1, 2, 3], ctx=mx.gpu(gpu_number))
    except mx.MXNetError:
        return None
    return mx.gpu(gpu_number)

class Infer:
    Batch = namedtuple('Batch', ['data'])
    epoch = 0
    thresh = 0.5
    data_shape = 512
    batch_size = 1
    prefix = '/ml/helmets/deploy_model_algo_1'
    network = 'resnet50'
    classes = ['safe', 'not_safe']
    colors = dict()

    def __init__(self):
        if gpu_device():
            ctx = mx.gpu()
        else:
            ctx = mx.cpu()

        sym, args, auxs = mx.model.load_checkpoint(self.prefix, self.epoch)
        self.mod = mx.mod.Module(sym, label_names=None, context=ctx)
        self.mod.bind( data_shapes=[('data', (1, 3, self.data_shape, self.data_shape))] )
        self.mod.set_params(args, auxs, allow_missing=True)

    def do(self, frame):
        height, width = frame.shape[:2]
        crop = (width - height) /2
        frame = frame[crop:crop+height, 0:height]
        frame = cv2.resize(frame, (self.data_shape, self.data_shape))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        img = mx.nd.array(frame)
        img = img.transpose((2, 0, 1))
        img = img.expand_dims(axis=0)
        
        self.mod.forward(self.Batch([img]))
        prob = self.mod.get_outputs()[0].asnumpy()[0]
        prob = np.squeeze(prob)

        return prob[:1]

    def visualize(self, dets, frame):
        global colors
        font = cv2.FONT_HERSHEY_DUPLEX
        size = 2
        thresh = 0.60
        count = 5
        i = 0
        results = []

        for det in dets:
            if i >= count:
                break
            i += 1
            (klass, score, x0, y0, x1, y1) = det
            if score < thresh:
                continue
            cls_id = int(klass)
            if cls_id not in self.colors:
                self.colors[cls_id] = (random.random(), random.random(), random.random())
            xmin = int(x0 * 512)
            ymin = int(y0 * 512)
            xmax = int(x1 * 512)
            ymax = int(y1 * 512)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), self.colors[cls_id], 2)

            class_name = str(cls_id) + ' - ' + str(score)
            if self.classes and len(self.classes) >= cls_id:
                class_name = self.classes[cls_id]

            cv2.putText(frame, class_name, (xmin, ymin), font, 1.0, self.colors[cls_id]) 
            results.append({'class': class_name, 'score': str(score)})
        return results