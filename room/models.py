from django.db import models
from users.models import User
from uuid import uuid4
from django.dispatch import receiver
from django.db.models.signals import post_save

class Room (models.Model) : 
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(User, related_name='user_room' ,on_delete=models.CASCADE)
    total_msgs = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.full_name + ' room'


class Message (models.Model):
    content = models.TextField()
    room = models.ForeignKey(Room, related_name='msg_room', on_delete=models.CASCADE)
    username = models.CharField(max_length=225)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self) -> str:
        return self.content
    
