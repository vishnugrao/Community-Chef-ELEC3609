from django.db import models

from chef.models import Chef
from customer.models import Customer

class ChatRoom(models.Model):
    id = models.TextField(primary_key=True)

    chef_id = models.ForeignKey(Chef, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    

class Message(models.Model):
    chat_room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.IntegerField()
