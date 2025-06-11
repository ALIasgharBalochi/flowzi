from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)
    nikname = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=100,blank=True, null=True)
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


