from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"User {user.id} connected to WebSocket notifications.")  # Debugging

    async def disconnect(self, close_code):
        """Remove user from notification group when they disconnect."""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"User {self.scope['user'].id} disconnected from WebSocket.")  # Debugging

    async def send_notification(self, event):
        """Send notification message to WebSocket client."""
        message = event["message"]
        print(
            f"Sending notification to user {self.scope['user'].id}: {message}"
        )  # Debugging
        await self.send(text_data=json.dumps({"message": message}))
    
    async def receive(self, text_data):
        """Receive WebSocket messages (for debugging)."""
        print(f" Received WebSocket message: {text_data}") 
