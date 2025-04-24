
from channels.generic.websocket import WebsocketConsumer 
from channels.generic.websocket import SyncConsumer
from asgiref.sync import async_to_sync


class Fconsumer(SyncConsumer):
    def websocket_connect(self,event):
        print(f'[{self.channel_name}] - Connected')
        self.room_name = 'lobby'
        self.send(
            {'type' : "websocket.accept"}
        )
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
    
    def websocket_receive(self, event):
        print(f'[{self.channel_name}] - Message received - {event.get("text")}')
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'websocket.message',
            'text': event.get('text')
            })
    
    def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message sent - {event.get("text")}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')})

    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disconnected')
        async_to_sync(self.channel_layer.group_discard)("lobby",self.channel_name)