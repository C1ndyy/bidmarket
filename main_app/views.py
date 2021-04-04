from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Listing, Bid
from django.contrib.auth.models import User

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


def listings_index(request):
    items = Listing.objects.all()

    bids = Bid.objects.all()
    for item in items:
        bids = Bid.objects.get(bid.listing=item.name):
            # for bid in bids:
            #     if str(bid.listing) == item.name:
            print(bid.bidder)
            print(bid.listing)

    return render(request, 'listings/index.html',
                  {'items': items, 'bids': bids},
                  )
