import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model() 

class PrivateChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user1 = models.ForeignKey(User, related_name='chats_initiated', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chats_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"

    @staticmethod
    def get_or_create_room(user_a, user_b):
        user1, user2 = sorted([user_a, user_b], key=lambda u: u.id)
        room, created = PrivateChatRoom.objects.get_or_create(user1=user1, user2=user2)
        return room


class PrivateMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    room = models.ForeignKey(PrivateChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} @ {self.created_at}: {self.message[:20]}"


# class Group(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     group_image = models.ImageField(upload_to='group_images/',blank=True,null=True)
#     admin = models.ForeignKey(User, related_name='admin_groups', on_delete=models.CASCADE)
#     is_private = models.BooleanField(default=False)
#     access_key = models.CharField(max_length=128, blank=True, null=True)  # You can hash it
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class GroupMembership(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('group', 'user')


# class Channel(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     channel_image = models.ImageField(upload_to='chanel_images/',blank=True,null=True)
#     admin = models.ForeignKey(User, related_name='admin_channels', on_delete=models.CASCADE)
#     is_private = models.BooleanField(default=False)
#     access_key = models.CharField(max_length=128, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class ChannelMembership(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
#     channel = models.ForeignKey(Channel, related_name='memberships', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     joined_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('channel', 'user')
