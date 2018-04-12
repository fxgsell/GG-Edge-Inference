import os
import greengrasssdk
from threading import Timer
import time
import cv2
from threading import Thread
import base64
import load_model
import logging

# Creating a greengrass core sdk client
GGC = greengrasssdk.client('iot-data')
IOT_TOPIC = 'inference/resnet'
MODEL_PATH = '/trained_model/ssd_resnet50_512/'
NETWORK_PATH = MODEL_PATH + 'ssd_resnet50_512'

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def open_cam_usb(dev):
    return cv2.VideoCapture(dev)

cap = open_cam_usb(1)

if not cap.isOpened():
    GGC.publish(topic=IOT_TOPIC, payload='Error failed to open camera')
    sys.exit("Failed to open camera!")
else:
    GGC.publish(topic=IOT_TOPIC, payload='Initilized camera successfully')
    
ret, frame = cap.read()
ret, jpeg = cv2.imencode('.jpg', frame)
Write_To_FIFO = True
class FIFO_Thread(Thread):
    def __init__(self):
        ''' Constructor. '''
        Thread.__init__(self)

    def run(self):
        fifo_path = "/tmp/results.mjpeg"
        if not os.path.exists(fifo_path):
            os.mkfifo(fifo_path)
        f = open(fifo_path, 'w')
        GGC.publish(topic=IOT_TOPIC, payload="Opened Pipe")
        while Write_To_FIFO:
            try:
                f.write(jpeg.tobytes())
            except IOError as e:
                continue


def inf_loop():
    try:
        global_model = load_model.ImagenetModel(NETWORK_PATH)
        modelType = "ssd"
        input_width = 300
        input_height = 300
        prob_thresh = 0.25
        results_thread = FIFO_Thread()
        results_thread.start()

        # Send a starting message to IoT console
        GGC.publish(topic=IOT_TOPIC, payload="Face detection starts now")

        ret, frame = cap.getLastFrame()
        if ret == False:
            raise Exception("Failed to get frame from the stream")

        yscale = float(frame.shape[0]/input_height)
        xscale = float(frame.shape[1]/input_width)

        doInfer = True
        while doInfer:
            # Get a frame from the video stream
            ret, frame = cap.read()
            # Raise an exception if failing to get a frame
            if ret == False:
                raise Exception("Failed to get frame from the stream")


            # Resize frame to fit model input requirement
            frameResize = cv2.resize(frame, (input_width, input_height))

            # Run model inference on the resized frame
            inferOutput = model.doInference(frameResize)

            # Output inference result to the fifo file so it can be viewed with mplayer
            parsed_results = model.parseResult(modelType, inferOutput)['ssd']
            label = '{'
            for obj in parsed_results:
                if obj['prob'] < prob_thresh:
                    break
                xmin = int( xscale * obj['xmin'] ) + int((obj['xmin'] - input_width/2) + input_width/2)
                ymin = int( yscale * obj['ymin'] )
                xmax = int( xscale * obj['xmax'] ) + int((obj['xmax'] - input_width/2) + input_width/2)
                ymax = int( yscale * obj['ymax'] )


                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 165, 20), 4)
                label += '"{}": {:.2f},'.format(str(obj['label']), obj['prob'] )
                label_show = '{}: {:.2f}'.format(str(obj['label']), obj['prob'] )
                cv2.putText(frame, label_show, (xmin, ymin-15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 20), 4)
            label += '"null": 0.0'
            label += '}'
            #GGC.publish(topic=IOT_TOPIC, payload = label)
            global jpeg
            ret,jpeg = cv2.imencode('.jpg', frame)

    except Exception as e:
        msg = "Test failed: " + str(e)
        GGC.publish(topic=IOT_TOPIC, payload=msg)

    Timer(1, inf_loop).start()

inf_loop()
# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return