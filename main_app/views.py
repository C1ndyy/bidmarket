from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Listing, Bid, Thread, Message, CATEGORIES, Photo
from datetime import date, datetime
from django.contrib.auth.models import User
from django.db.models import Count
import uuid
import logging #TEMP
import boto3
from botocore.exceptions import ClientError #TEMP
import os #<-----environment variables 
import environ #<-----environment variables 
environ.Env() #<-----environment variables
environ.Env.read_env() #<-----environment variables 

# to use your own S3 bucket, place your definitions in your .env file
S3_BASE_URL = os.environ['S3_BASE_URL']
BUCKET = os.environ['BUCKET']
AWS_ACCESS_ID = os.environ['AWS_ACCESS_ID']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']




# Create your views here.


def home(request):
    hottest_listings = Listing.objects.annotate(number_of_bids = Count('bid')).order_by('-number_of_bids')[:10]
    ending_soon_listings = Listing.objects.order_by('expiry_date')[:10]
    return render(request, 'home.html', {'hottest_listings': hottest_listings, 'ending_soon_listings': ending_soon_listings})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
            print(form.errors)
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

#----------------------------------Messaging---------------------------------#
@login_required
def message_index(request):
    threads = Thread.objects.filter(user1__id=request.user.id) | Thread.objects.filter(user2__id=request.user.id)
    # filters out threads with 0 messages
    threads = threads.annotate(number_of_messages=Count('message')).filter(number_of_messages__gt=0)
    return render(request, 'messages/index.html', {'threads': threads, 'userid': request.user.id})

@login_required
def message_detail(request, thread_id):
    user_id = request.user.id
    thread = Thread.objects.get(id=thread_id)
    other_user = thread.user1 if thread.user1.id != user_id else thread.user2      
    messages = Message.objects.filter(parent_thread__id=thread_id).order_by('datetime')
    return render(request, 'messages/detail.html', 
    {'messages': messages, 
    'thread': thread, 
    'user_id': user_id, 
    'other_user': other_user})

@login_required
def send_message(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    thread.message_set.create(message= request.POST['message'], sender= request.user, datetime= datetime.now(),)    
    return redirect('message_detail', thread_id = thread_id)

@login_required
def new_message(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    listing_threads = Thread.objects.filter(listing__id = listing_id)
    existing_thread = listing_threads.filter(user1__id = request.user.id) | listing_threads.filter(user2__id=request.user.id)
    if existing_thread.exists():
        return redirect('message_detail', thread_id= existing_thread[0].id)
    else: 
        new_thread = Thread.objects.create(listing_id = listing_id, user1_id= listing.seller_id, user2_id = request.user.id)
        return redirect('message_detail', thread_id= new_thread.id)

#----------------------------------Listings---------------------------------#


def listings_index(request):
    # query by keyword
    q=request.GET.get('q', '')
    items = Listing.objects.filter(name__icontains=q)
    # filter by category
    category = request.GET.get('category', '')
    items = items.filter(category__icontains=category)
    #sort options
    sortby = request.GET.get('sortby')
    if sortby == 'price-LH':
        items = items.order_by("current_highest_bid")
    elif sortby == 'price-HL':
        items = items.order_by("-current_highest_bid")
    elif sortby == 'oldest-first':
        items = items.order_by("created_date")
    elif sortby == 'newest-first':
        items = items.order_by("-created_date")
    else:
        items = items.order_by("expiry_date")
    return render(request, 'listings/index.html', 
    {'items': items, 
    'q': q, 
    'sortby': sortby, 
    'category': category})

@login_required
def profile(request):
    listings = Listing.objects.filter(seller__id=request.user.id)
    bids = Bid.objects.filter(bidder__id=request.user.id).order_by('-datetime')
    return render(request, 'profile.html', {'listings': listings, 'username': request.user.username, 'bids': bids})


def listings_create(request):
    return render(request, 'listings/create.html', 
    {"categories": CATEGORIES}
    )


#now has websocket functionality
def listings_detail(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    room_name = str(listing_id)
    return render(request, 'listings/detail.html', 
    {
        'item': item,
        'room_name': room_name,
        'user': request.user
    })

@login_required
def listings_update(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    return render(request, 'listings/update.html', 
    {'item': item,})



@login_required
def listings_delete(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    item.delete()
    response = redirect('/listings/')
    return response


# AWS s3 photo upload:
def photo_upload(request, item_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_ID,
            aws_secret_access_key=AWS_ACCESS_KEY,
        )
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, listing_id=item_id)
            photo.save()
        except ClientError as e:
            print(e)


def add_photo(request, listing_id):
    photo_upload(request, listing_id)
    response = listings_update(request, listing_id)
    return response

def update_item(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    item.name = request.POST.get("name")
    item.address = request.POST.get("address")
    item.description = request.POST.get("description")
    item.expiry_date = request.POST.get("expiry_date")
    item.save()
    response = redirect('/listings/')
    return response


def delete_photo(request, photo_id,):
    photo = Photo.objects.get(id=photo_id)
    listing_id = photo.listing_id
    photo.delete()
    response = listings_update(request, listing_id)
    return response

@login_required
def listings_new(request):
    photo_file = request.FILES.get('photo-file', None)
    item = Listing(name=request.POST.get("name"),
    seller_id=request.user.id,
    description=request.POST.get("description"),
    address=request.POST.get("address"),
    category=request.POST.get("category"),
    min_bid_price=int(request.POST.get("min_bid_price")),
    current_highest_bid=int(request.POST.get("min_bid_price")),
    buy_now_price=int(request.POST.get("buy_now_price")),
    created_date=datetime.now(),
    expiry_date=request.POST.get("expiry_date"),
    )
    item.save()
    photo_upload(request, item.id)
    response = redirect('/listings/')
    return response
