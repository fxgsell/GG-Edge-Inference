import platform
import greengrasssdk
import json
from inspect import currentframe

class Publisher:
    def __init__(self, admin, main, thing):
        self.admin = admin
        self.main = main
        self.thing = thing

        if platform.system() != 'Darwin':
            GGC = greengrasssdk.client('iot-data')
            def debug(topic=self.admin, payload=""):
                GGC.publish(topic=topic, payload=payload)
            self.publish = debug
        else:
            def debug(topic=self.admin, payload=""):
                print(topic, payload)
            self.publish = debug

    def exception(self, err):
        self.publish(topic=self.admin, payload=json.dumps({
            "type":  "exception",
            "thing": self.thing,
            "location": currentframe().f_back.f_filename,
            "line": currentframe().f_back.f_lineno,
            "payload": err
        }))

    def info(self, data):
        self.publish(topic=self.admin, payload=json.dumps({
            "type":  "info",
            "thing": self.thing,
            "payload": data
        }))

    def events(self, data):
        self.publish(topic=self.admin, payload=json.dumps({
            "type":  "event",
            "thing": self.thing,
            "count": len(data),
            "payload": data
        }))


