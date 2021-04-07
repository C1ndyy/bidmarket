# bid/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Listing, Bid
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class BidConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'bid_%s' % self.room_name
        print("group name: " + self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        listingId = text_data_json['listingId']
        userId = text_data_json['userId']

        #construct new bid, store in database
        #set highest bid
        print("recieve step 1")
        listingId = int(listingId)
        userId = int(userId)
        value = int(message)

        listing_item = await database_sync_to_async(Listing.objects.get)(id = listingId)
        bidding_user = await database_sync_to_async(User.objects.get)(id = userId)
        new_bid = await database_sync_to_async(Bid)(listing = listing_item, bidder = bidding_user, amount = value)
        await database_sync_to_async(new_bid.save)()

        if new_bid.amount > listing_item.current_highest_bid:
            listing_item.current_highest_bid = new_bid.amount
       
        highest_bid = listing_item.current_highest_bid
        await database_sync_to_async(listing_item.save)()
       
      
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'bid_message',
                'message': message,
                'username': username,
                'highest_bid': highest_bid
            }
        )
        
    

    # Receive message from room group
    async def bid_message(self, event):
        print("bid_message step 1")
        message = event['message']
        username = event['username']
        highest_bid = event['highest_bid']
        print('bid_message step 2')
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'highest_bid': highest_bid
            
        }))
        print('bid message complete')