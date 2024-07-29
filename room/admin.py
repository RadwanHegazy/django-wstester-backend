from django.contrib import admin
from .models import Room, Message

@admin.register(Room)
class RoomPanel (admin.ModelAdmin) :
    list_display = ['user','id','total_msgs','total_users']


@admin.register(Message)
class MessagePanel (admin.ModelAdmin) :
    list_display = ['username','room','content']