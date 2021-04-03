from django.contrib import admin

# Register your models here.
from .models import Listing, Bid

myModels = [Listing, Bid]
admin.site.register(myModels)
