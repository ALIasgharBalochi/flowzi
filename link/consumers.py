import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import PrivateChatRoom, PrivateMessage

User = get_user_model()

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        self.me = self.scope["user"]
        self.other_user = await self.get_user_by_id(self.other_user_id)
        self.room = await self.get_or_create_room(self.me, self.other_user)

        self.room_group_name = f"pv_{self.room.id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # ارسال پیام‌های قبلی
        messages = await self.get_past_messages(self.room)
        for msg in reversed(messages):
            await self.send(text_data=json.dumps({
                'sender': await self.get_username(msg.sender),
                'message': msg.message_for_sender if msg.sender == self.me else msg.message_for_receiver,
                'created_at': msg.created_at.isoformat()
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_sender = data.get('message_for_sender')
        msg_receiver = data.get('message_for_receiver')

        # ذخیره در دیتابیس
        new_msg = await self.create_message(
            self.room,
            self.me,
            msg_sender,
            msg_receiver
        )

        # ارسال به همه اعضای گروه
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': self.me.username,
                'message_for_sender': msg_sender,
                'message_for_receiver': msg_receiver,
                'created_at': new_msg.created_at.isoformat()
            }
        )

    async def chat_message(self, event):
        current_user = self.scope["user"]
        message = event["message_for_sender"] if current_user == self.me else event["message_for_receiver"]

        await self.send(text_data=json.dumps({
            'sender': event["sender"],
            'message': message,
            'created_at': event["created_at"]
        }))

    # ---------- Sync-to-Async Helpers ----------

    @sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    @sync_to_async
    def get_or_create_room(self, user1, user2):
        return PrivateChatRoom.get_or_create_room(user1, user2)

    @sync_to_async
    def get_past_messages(self, room):
        return list(room.messages.select_related('sender').order_by('-created_at')[:50])

    @sync_to_async
    def get_username(self, user):
        return user.username

    @sync_to_async
    def create_message(self, room, sender, message_sender, message_receiver):
        return PrivateMessage.objects.create(
            room=room,
            sender=sender,
            message_for_sender=message_sender,
            message_for_receiver=message_receiver
        )
