from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class PlaylistConsumer(WebsocketConsumer):
    def connect(self):
        self.playlist_name = self.scope['url_route']['kwargs']['pk']
        self.playlist_group_name = 'playlist_%s' % self.playlist_name

        async_to_sync(self.channel_layer.group_add)(
            self.playlist_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.playlist_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.playlist_group_name,
            {
                'type': 'message',
                'message': message
            }
        )

    def message(self, event):
        message = event['message']
        print(message)
        self.send(text_data=json.dumps({
            'message': message
        }))
