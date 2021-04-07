from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Listing, Bid, Thread, Message, CATEGORIES, Photo
from datetime import date, datetime
from django.contrib.auth.models import User
import uuid
import boto3
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
    return render(request, 'home.html')


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

@login_required
def message_index(request):
    threads = Thread.objects.filter(user1__id=request.user.id) | Thread.objects.filter(user2__id=request.user.id)
    return render(request, 'messages/index.html', {'threads': threads})

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

@login_required
def listings_new(request):
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
    response = redirect('/listings/')
    return response

#now has websocket functionality

def listings_detail(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    room_name = str(listing_id)
    return render(request, 'listings/detail.html', 
    {
        'item': item,
        'room_name': room_name
    })

@login_required
def listings_update(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    item_info = {
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'address': item.address,
        'min_bid_price': item.min_bid_price,
        'buy_now_price': item.buy_now_price,
        'expiry_date': item.expiry_date,
    }   
    return render(request, 'listings/update.html', 
    {'item': item,
    'item_info': item_info,})



@login_required
def listings_delete(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    item.delete()
    response = redirect('/listings/')
    return response

#websocket room
def room(request, room_name):
    return render(request, 'biddingroom.html', {
        'room_name': room_name
    })

# AWS s3 photo upload:

def add_photo(request, listing_id):
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
            photo = Photo(url=url, listing_id=listing_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('listings_update', listing_id=listing_id)