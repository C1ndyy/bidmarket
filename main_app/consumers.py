from channels.generic.websocket import AsyncWebsocketConsumer
import json
class  BidRoomConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'bid_%s' % self.room_name
        print("BidRoomConsumer connect function activate, room_group_name = " + self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
  
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def recieve(Self, text_data):
        #print("BidRoomconsumer recieve function activate")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'bid_message',
                'message': message
            }
        )
        
    async def bid_mesage(self, event):
        print("BidRoomConsumer bid_message function activate")
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
    pass