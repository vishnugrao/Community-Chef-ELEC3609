import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatRoom, Message

from chef.models import Chef
from customer.models import Customer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message", 
                "message": message, 
                "sender": self.scope["user"].username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))

    @database_sync_to_async
    def save_message(self, message):
        ids = self.room_id.split("_")

        print(chef_id := int(ids[0]))
        print(customer_id := int(ids[1]))

        chef = Chef.objects.get(id = chef_id)
        customer = Customer.objects.get(id = customer_id)

        print(chef)
        print(customer)

        newRoom, created = ChatRoom.objects.get_or_create(id=self.room_id, chef_id=chef, customer_id=customer)
        newRoom.save()

        print(newRoom)

        user = 0
        if self.scope["user"].id is not None:
            user = self.scope["user"].id

        newMsg = Message(chat_room_id=newRoom, message=message, sender=user)
        newMsg.save()


