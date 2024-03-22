from channels.consumer import SyncConsumer 
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Fconsumer(SyncConsumer):
    def websocket_connect(self,event):
        self.send(
            {'type' : "websocket.accept"}
        )
        async_to_sync(self.channel_layer.group_add)("room_name","channel_name")
        print(f'[channel name] - you are connected')
    def websocket_receive(self,event):
        print(event)
        self.send(
            {'type' : "websocket.send",
             'text' : event.get('text')
            })

    def websocket_disconnect(self, event):
        print("disconnected")
        print(event)
