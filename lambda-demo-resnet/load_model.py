''''''
import urllib2
import cv2
import argparse
import time
from collections import namedtuple
import numpy as np
import mxnet as mx

Batch = namedtuple('Batch', ['data'])

class ImagenetModel(object):
    #Loads a pre-trained model locally 
    #and returns an MXNet graph that is ready for prediction
    def __init__(self, synset_path, network_prefix, context=mx.gpu()):
        batch_size = 1
        data_shape = 512
        label_names=None

        # Load the symbols for the networks
        # self.synsets  = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
        self.synsets  = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
                        'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 
                        'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

        # Load the network parameters from default epoch 0
        sym, arg_params, aux_params = mx.model.load_checkpoint(network_prefix, 0)

        # Load the network into an MXNet module and bind the corresponding parameters
        self.mod = mx.mod.Module(symbol=sym, label_names=label_names, context=context)
        self.mod.bind(data_shapes=[('data', (batch_size, 3, data_shape, data_shape))])
        self.mod.set_params(arg_params, aux_params)

    def predict_from_image(self, cvimage, reshape=(416, 416), N=5):
        topN = []

        # Switch RGB to BGR format (which ImageNet networks take)
        img = cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB)
        if img is None:
            return topN

        # Resize image to fit network input
        img = cv2.resize(img, reshape)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 1, 2)
        img = img[np.newaxis, :]

        # Run forward on the image
        self.mod.forward(Batch([mx.nd.array(img)]))
        prob = self.mod.get_outputs()[0].asnumpy()
        prob = np.squeeze(prob)
        return prob
        # Extract the top N predictions from the softmax output
        # a = np.argsort(prob)[::-1]
        # for i in a[0:N]:
        #    topN.append((prob[i], self.synsets[i]))
        # return topN
