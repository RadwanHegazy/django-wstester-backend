from rest_framework import serializers
from ..models import Message

class MsgSerializer (serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['username','content','sent_at']

    def to_representation(self, instance:Message):
        data = super().to_representation(instance)
        data['sent_at'] = instance.sent_at.strftime("%d/%m/%Y, %H:%M:%S")
        return data