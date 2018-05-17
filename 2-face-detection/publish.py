import platform
import greengrasssdk

IOT_TOPIC = 'jetson/inference'
IOT_TOPIC_ADMIN = 'jetson/admin'

if platform.system() != 'Darwin':
    GGC = greengrasssdk.client('iot-data')
    def debug(topic=IOT_TOPIC_ADMIN, payload=""):
        GGC.publish(topic=topic, payload=payload)
    publish = debug
else:
    def debug(topic=IOT_TOPIC_ADMIN, payload=""):
        print(topic, payload)
    publish = debug
