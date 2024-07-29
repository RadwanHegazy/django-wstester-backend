from channels.generic.websocket import WebsocketConsumer
from ..models import Room, Message
from ..apis.serializers import MsgSerializer
import json
from asgiref.sync import async_to_sync


class RoomConsumer (WebsocketConsumer) : 
    errors = []

    def connect (self) :
        self.accept()
        room_id = self.scope['url_route']['kwargs']['room_id']
        try : 
            self.room = Room.objects.get(id=room_id)
        except Exception:
            self.close()
            return
        
        msgs = Message.objects.filter(room=self.room)
        msg_serializer = MsgSerializer(msgs, many=True)
        data = {
            'type' : 'msgs' ,
            'msgs' : msg_serializer.data
        }
        self.send(text_data=json.dumps(data))

        self.GROUP_NAME = f'room_{room_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME,
            self.channel_name
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME,
            self.channel_name
        )

    def receive(self, text_data):
        user_data = json.loads(text_data)
        valid_data = self.check_data(user_data)
        if not valid_data : 
            self.send(json.dumps({
                'type' : 'error',
                'errors' : self.errors
            }))
            return
        
        message = Message.objects.create(
            room=self.room,
            username = user_data['username'],
            content = user_data['content'],
        )

        message.save()

        serializer = MsgSerializer(message)
        async_to_sync(self.channel_layer.group_send)(
            self.GROUP_NAME,
            {
                'type' : 'send.group.msg',
                'event' : serializer.data
            }
        )
        
    def send_group_msg (self, event) : 
        data = {
            'type' : 'msg',
            'data' : event['event']
        }
        self.send(text_data=json.dumps(data))
    
    def check_data (self, data:dict) : 
        username = data.get('username', None)
        content = data.get('content', None)

        if username is None:
            self.errors.append({
                'username' : 'field not found'
            })
            return False
        
        if content is None:
            self.errors.append({
                'content' : 'field not found'
            })
            return False
        
        return True