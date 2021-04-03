from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

CATEGORIES = (
    ("Home","Home"),
    ("Fasion","Fasion"),
    ("Tech","Tech"),
    ("Sporting","Sporting"),
    ("Books","Books"),
)
class Listing(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    address = models.CharField(max_length=50)
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

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    datetime = models.DateTimeField()

    def __str__(self):
        return self.name

