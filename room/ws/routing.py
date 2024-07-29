from .consumer import RoomConsumer
from django.urls import path

urlpatterns = [
    path('ws/room/<str:room_id>/', RoomConsumer.as_asgi())
]