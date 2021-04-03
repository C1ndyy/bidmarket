from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Listing, Bid, Thread, Message

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
    print(request.user.id)
    print(Thread.objects.all())
    threads = Thread.objects.filter(user1__id=request.user.id) | Thread.objects.filter(user2__id=request.user.id)

    return render(request, 'messages/index.html', {'threads': threads})

def listings_index(request):
    items = Listing.objects.all()
    return render(request, 'listings/index.html', {'items': items})
