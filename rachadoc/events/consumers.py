from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class EventstConsumer(JsonWebsocketConsumer):
    def connect(self):
        if not "user" in self.scope or not self.scope["user"].is_active:
            self.close()
        if "clinic_id" not in self.scope or self.scope["clinic_id"] is None:
            self.close()
        async_to_sync(self.channel_layer.group_add)(self.scope["clinic_id"], self.channel_name)
        return super().connect()

    def receive_json(self, content, **kwargs):
        pass

    def send_updates(self, data):
        appointement = data["data"]
        self.send_json(appointement)

    def disconnect(self, code):
        if "clinic_id" in self.scope:
            async_to_sync(self.channel_layer.group_discard)(self.scope["clinic_id"], self.channel_name)
        return super().disconnect(code)
