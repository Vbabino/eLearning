from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user= self.scope.get("user")
        if not user or getattr(user, "is_anonymous", True):
            await self.close()
        else:
            self.room_group_name = "chat_room"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_id = data.get("sender_id")

        if not sender_id:
            print("🚨 Received message missing sender_id:", data)
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({ "message": event["message"], "sender_id": event["sender_id"] }))
