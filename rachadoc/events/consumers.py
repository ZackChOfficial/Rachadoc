from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class EventstConsumer(JsonWebsocketConsumer):
    def connect(self):
        if not self.scope["user"].is_active or not self.scope["clinic"]:
            self.close()
        async_to_sync(self.channel_layer.group_add)(self.scope["clinic"], self.channel_name)
        return super().connect()

    def receive_json(self, content, **kwargs):
        pass

    def send_updates(self, data):
        appointement = data["data"]
        self.send_json(appointement)

    def disconnect(self, code):
        if self.scope["clinic"]:
            async_to_sync(self.channel_layer.group_discard)(self.scope["clinic"], self.channel_name)
        return super().disconnect(code)
