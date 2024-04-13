from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import ChatRoom, Message

class ChatRoomTests(TestCase):
    def test_multiple_chat_rooms(self):
        room = ChatRoom(id="test1")
        room2 = ChatRoom(id="test2")

        self.assertTrue(room != room2)

    def test_large_number_chat_rooms(self):
        room = ChatRoom(id="test1")
        room2 = ChatRoom(id="test2")
        room3 = ChatRoom(id="test3")
        room4 = ChatRoom(id="test4")
        room5 = ChatRoom(id="test5")

        self.assertTrue(room != room2)
        self.assertTrue(room3 != room4)
        self.assertTrue(room4 != room5)
        self.assertTrue(room2 != room3)

    def test_multiple_messages(self):
        room = ChatRoom(id="test1")

        message1 = Message(chat_room_id=room, message="hello", timestamp=timezone.now(), sender=1)
        message2 = Message(chat_room_id=room, message="hello back", timestamp=timezone.now(), sender=2)

        self.assertTrue(message2.chat_room_id == message1.chat_room_id)
        self.assertTrue(message1 != message2)

    def test_multiple_chat_rooms_multiple_messages(self):
        room = ChatRoom(id="test1")

        message1 = Message(chat_room_id=room, message="hello", timestamp=timezone.now(), sender=1)
        message2 = Message(chat_room_id=room, message="hello back", timestamp=timezone.now(), sender=2)

        room2 = ChatRoom(id="test2")
        message3 = Message(chat_room_id=room2, message="different hello", timestamp=timezone.now(), sender=1)
        message4 = Message(chat_room_id=room2, message="different hello back", timestamp=timezone.now(), sender=3)

        self.assertTrue(message1.chat_room_id != message3.chat_room_id)
        self.assertTrue(message3.chat_room_id == message4.chat_room_id)

        self.assertTrue(message1.sender == message3.sender)
        self.assertTrue(message2.sender != message1.sender)

    def test_chat_room_viewable(self):
        response = self.client.get(reverse("room", args="r"))
        self.assertEqual(response.status_code, 302)


