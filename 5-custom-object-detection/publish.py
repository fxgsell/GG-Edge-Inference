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
            def debug(topic=self.admin, payload={}):
                payload['thing'] = self.thing
                GGC.publish(topic=topic, payload=json.dumps(payload))
            self.publish = debug
        else:
            def debug(topic=self.admin, payload={}):
                payload['thing'] = self.thing
                print(topic, json.dumps(payload))
            self.publish = debug

    def exception(self, err):
        self.publish(topic=self.admin, payload={
            "type":  "exception",
#            "location": currentframe().f_back.f_filename,
            "line": currentframe().f_back.f_lineno,
            "payload": err
        })

    def info(self, data):
        self.publish(topic=self.admin, payload={
            "type":  "info",
            "payload": data
        })

    def events(self, data):
        if len(data) == 0:
            return

        self.publish(topic=self.main, payload={
            "type":  "events",
            "count": len(data),
            "payload": data
        })


