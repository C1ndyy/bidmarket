from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

CATEGORIES = (
    ("Home","Home"),
    ("Fashion","Fashion"),
    ("Tech","Tech"),
    ("Sporting","Sporting"),
    ("Books","Books"),
)
class Listing(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    address = models.CharField(max_length=50)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    min_bid_price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    buy_now_price= models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    current_highest_bid = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    created_date = models.DateTimeField()
    expiry_date = models.DateTimeField()

    def __str__(self):
        return self.name

    def time_remaining(self):
        difference=self.expiry_date-timezone.now()
        if difference.days > 0:
            return f'{difference.days}d {difference.seconds//3600}h'
        else:
            return f'{difference.seconds//3600}h {(difference.seconds//60)%60}m'
    
    def number_of_bids(self):
        return self.bid_set.filter(listing__id=self.id).count()

    def bids(self):
        return self.bid_set.all().order_by('-datetime')

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    datetime = models.DateTimeField(default=datetime.now, blank=True)
    # datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.listing)

class Thread(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user1 = models.ForeignKey(User,related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User,related_name="user2", on_delete=models.CASCADE)

    def latest_message(self):
        return self.message_set.all().order_by('-datetime')[0].message
    
    def latest_message_date(self):
        return self.message_set.all().order_by('-datetime')[0].datetime

class Message(models.Model):
    parent_thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    datetime = models.DateTimeField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)


class Photo(models.Model):
    url = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Photo for listing_id: {self.listing_id} @{self.url}"
        