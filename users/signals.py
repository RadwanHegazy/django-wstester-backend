from .models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from room.models import Room

@receiver(post_save, sender=User)
def create_user_room(instance, created, **kwargs) : 
    if not created:
        return
    
    Room.objects.create(
        user=instance
    ).save()