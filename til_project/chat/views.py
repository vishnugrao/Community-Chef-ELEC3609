from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Message, ChatRoom
from chef.models import Chef
from customer.models import Customer

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

LOGIN_URL = "/"

# Create your views here.
def index(request):
    return render(request, "chat/index.html")

@login_required(login_url=LOGIN_URL)
def room(request, room_id):
    history = Message.objects.filter(chat_room_id=room_id).order_by("timestamp")

    for message in history:
        if message.sender == 0:
            message.sender = "Anonymous"
        else:
            message.sender = User.objects.get(id=message.sender).username

    return render(request, "chat/room.html", {"room_id": room_id, "history": history})