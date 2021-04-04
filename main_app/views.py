from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Listing, Bid, Thread, Message
from datetime import datetime

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
    items = Listing.objects.all()
    return render(request, 'listings/index.html', {'items': items})
