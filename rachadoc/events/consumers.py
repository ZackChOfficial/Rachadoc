import json
from channels.generic.websocket import JsonWebsocketConsumer


class EventstConsumer(JsonWebsocketConsumer):
    def connect(self):

        return super().connect()

    def receive_json(self, content, **kwargs):
        message_type = content.get("action")
        if message_type == "appointement.create":
            pass
        elif message_type == "appointement.update":
            pass

    def disconnect(self, code):
        return super().disconnect(code)
