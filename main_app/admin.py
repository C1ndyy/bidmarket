from django.contrib import admin
from .models import Listing, Bid, Thread, Message

# Register your models here.
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Thread)
admin.site.register(Message)
