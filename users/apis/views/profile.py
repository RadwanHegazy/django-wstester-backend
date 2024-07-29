from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from room.models import Room
from django.http import HttpRequest

class ProfileView (APIView) :
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request:HttpRequest) : 
        user = request.user
        room = Room.objects.get(user=user)
        ws = request.get_host()
        
        if request.scheme == 'http' : 
            ws = 'ws://' + ws
        elif request.scheme == 'https' : 
            ws = 'wss://' + ws
        
        data = {
            'id' : user.id,
            'full_name' : user.full_name,
            'email' : user.email,
            'room' : {
                'url' : f'{ws}/ws/room/{room.id}/',
                'msgs' : room.total_msgs,
                'users' : room.total_users,
            }
        }
        return Response(data, status=status.HTTP_200_OK)