from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from chatting.models import Message


class ChatConsumer(WebsocketConsumer):
    # websocket 연결 시 실행
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chatting_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    # websocket 연결 종료 시 실행
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 클라이언트로부터 메세지를 받을 시 실행
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 클라이언트로부터 받은 메세지를 다시 클라이언트로 보내준다.
    def chat_message(self, event):
        message = event['message']
        self.post_message(message=message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def post_message(self, message):
        Message.objects.create(text=message)