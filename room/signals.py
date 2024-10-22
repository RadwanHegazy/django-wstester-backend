from .models import Message, Room
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=Message)
def update_room_details (created, instance:Message, **kwargs) :
    if not created:
        return
    
    username = instance.username
    room = instance.room

    increes_users = Message.objects.filter(room=room, username=username).count() == 1
    
    if increes_users:
        room.total_users += 1
    
    room.total_msgs += 1
    room.save()


@receiver(post_delete, sender=Message)
def update_room_details_on_delete (instance, **kwargs) :
    room = instance.room
    room.total_msgs -= 1
    room.total_users -= 1
    room.save()