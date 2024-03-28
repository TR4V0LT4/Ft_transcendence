
from channels.generic.websocket import WebsocketConsumer 
from channels.generic.websocket import SyncConsumer
from asgiref.sync import async_to_sync
import json

players = []

class Fconsumer(SyncConsumer):
    # clients = []

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    # def websocket_connect(self,event):
    #     print(f'[{self.channel_name}] - Connected')
    #     self.room_name = 'lobby'
    #     self.send(
    #         {'type' : "websocket.accept"}
    #     )
    #     async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
    #     self.clients.append(self.channel_name)
    #     print('Clients:', self.clients)
    
    # def websocket_receive(self, event):
    #     print(f'[{self.channel_name}] - Message received - {event.get("text")}')
    #     text_data = event.get('text')
    #     if text_data:
    #         try:
    #             data = json.loads(text_data)
    #             if 'type' in data and data['type'] == 'getPlayers':
    #                 # Send the current players to the client
    #                 self.send({
    #                     'type': 'websocket.send',
    #                     'text': json.dumps({'type': 'players', 'players': players})
    #                 })
    #             elif 'player' in data:
    #                 players.append(data['player'])
    #                 print(f'[{self.channel_name}] - Player added - {data["player"]}')   
    #                 async_to_sync(self.channel_layer.group_send)(self.room_name, {
    #                     'type': 'websocket.message',
    #                     'text': json.dumps(players)
                    # })
        
    # //first consumer
    clients = []
    players = []
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def websocket_connect(self,event):
        if(len(self.clients) == 4):
            print("Room is full")
            self.send(
                {'type' : "websocket.close"}
            )
            return
        print(f'[{self.channel_name}] - Connected')
        self.room_name = 'lobby'
        self.send(
            {'type' : "websocket.accept"}
        )
        async_to_sync(self.channel_layer.group_add)(self.room_name,self.channel_name)
        self.clients.append(self.channel_name)
        
        player_number = len(self.clients)
        player_name = "P" + str(player_number)
        self.players.append(player_name)
        print("--------------->",player_name,self.players)
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'websocket.message',
                'text': json.dumps({'type': 'players', 'players': self.players})
            }
        )
    def websocket_receive(self, event):
        pass
        # print(f'[{self.channel_name}] - Message received - {event.get("text")}')
        # text_data = event.get('text')
        # if text_data:
        #     try:
        #         data = json.loads(text_data)
        #         if 'type' in data and data['type'] == 'getPlayers':
        #             # Send the current players to the client
        #             self.send({
        #                 'type': 'websocket.send',
        #                 'text': json.dumps({'type': 'players', 'players': players})
        #             })
        #         elif 'player' in data:
        #             players.append(data['player'])
        #             print(f'[{self.channel_name}] - Player added - {data["player"]}')   
        #             async_to_sync(self.channel_layer.group_send)(self.room_name, {
        #                 'type': 'websocket.message',
        #                 'text': json.dumps(players)
        #             })
        #         else:
        #             async_to_sync(self.channel_layer.group_send)(self.room_name, {
        #                 'type': 'websocket.message',
        #                 'text': text_data
        #             })
        #     except json.JSONDecodeError:
        #         print(f'Error parsing JSON: {text_data}')
    
    def websocket_message(self, event):
        print(f'[{self.channel_name}] - Message sent - {event.get("text")}')
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')})

    def websocket_disconnect(self, event):
        print(f'[{self.channel_name}] - Disconnected')
        async_to_sync(self.channel_layer.group_discard)("lobby",self.channel_name)