import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.user = self.scope["user"]
        print(self.user)
        if not self.user.is_anonymous:
            # If the user is authenticated, use their username
            self.username = self.user.email
        else:
            # If the user is not authenticated, use a default value or handle as needed
            self.username = "Anonymous"

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # user = request.user or None

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, "username": self.username}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # user = request.user or None
        sender_username = event.get("username", "Anonymous")


        # Send message to WebSocket
        self.send(text_data=json.dumps({"username":sender_username,"message": message,}))