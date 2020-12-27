from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from .models import *

from .models import User, Listing
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# class NewListingForm(forms.Form):
#     title = forms.CharField(label="Title", max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
#     description = forms.CharField(label="Description", max_length=255, widget=forms.Textarea(attrs={'class':'form-control'}))
#     active = forms.BooleanField(required = True,)
#     start_bid = forms.DecimalField(label="Starting Bid", max_digits=10, decimal_places=2)
#     category = forms.CharField(label="Category", max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))

#     # date = forms.DateTimeField(label="Date and Time")

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'active', 'image', 'start_bid', 'category']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'})
            # 'category': forms.TextInput(attrs={'class':'form-control'})

        }

"""
class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label="Description", max_length=255, widget=forms.Textarea(attrs={'class':'form-control'}))
    active = forms.BooleanField(required = True,)
    start_bid = forms.DecimalField(label="Starting Bid", max_digits=10, decimal_places=2)
    category = forms.CharField(label="Category", max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField()
    # date = forms.DateTimeField(label="Date and Time")
"""



def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if Watcher.objects.filter(user=request.user): 
                watcher = Watcher.objects.get(user=request.user)
                return render(request, "auctions/index.html", {
                    "listings" : Listing.objects.all(),
                    "watchlist_length": len(watcher.watchitems.all())
                })
            else:
                return render(request, "auctions/index.html", {
                    "listings" : Listing.objects.all(),
                    "watchlist_length": 0
                })

        else:
            print(request.user)
            return render(request, "auctions/index.html")
        

        


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    
    if request.method == 'GET':
        form = ListingForm()
        return render(request, "auctions/create.html", {
            "form": form
        })
    if request.method == 'POST':
        new_listing = Listing(user = request.user)
        form = ListingForm(request.POST, request.FILES, instance=new_listing)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))

@login_required
def get_listing(request, listing_id):
    

    #display close or bid button?
    current_user = request.user
    listing = Listing.objects.get(id=listing_id)
    lister = listing.user
    close = False
    if lister == current_user:
        close = True
    # process the users watchlist
    if not Watcher.objects.filter(user=request.user):
        new_watcher= Watcher(user = request.user)
        new_watcher.save()
    
    watcher = Watcher.objects.get(user=request.user)
    listing = Listing.objects.get(id=listing_id)
    status= None

    #retrieve comments for display
    comments = Comment.objects.filter(listing=listing)

    #did the current user win this auction
    if listing.active == False:
        status = listing.winner
    if request.method == 'GET':
        
        if not watcher.watchitems.filter(id= listing_id):

            return render(request, "auctions/listing_info.html", {
                "listing": listing,
                "watchlist": True,
                "close": close,
                "status": status,
                "comments": comments
                
            })
        else:
            return render(request, "auctions/listing_info.html", {
                "listing": listing,
                "watchlist": False,
                "close": close,
                "status": status,
                "comments": comments
                
            })
    if request.method == 'POST':
        action = request.POST["action"]
        if action == "add":
            watcher.watchitems.add(listing)
        elif action == "del":
            watcher.watchitems.remove(listing)
        return HttpResponseRedirect(reverse('get_listing', args=(listing_id,)))
    

@login_required
def watchlist(request):
    
    if request.method == 'GET':
        
        if Watcher.objects.filter(user=request.user):
            watcher = Watcher.objects.get(user=request.user)
            return render(request, "auctions/watchlist.html", { 
                "watchlist" : watcher.watchitems.all()
            })
        else:
            return render(request, "auctions/watchlist.html", { 
                "watchlist" : ""
            })

    
    if request.method == 'POST':
        watcher = Watcher.objects.get(user=request.user)
        item_id = request.POST["delitem"]
        selected = watcher.watchitems.get(id= item_id)
        watcher.watchitems.remove(selected)

        # watcher.watchitems.remove(id = item_id)

        return HttpResponseRedirect(reverse('watchlist'))

@login_required
def makeBid(request, listing_id):
    if request.method == 'POST':
        bid_amt = float(request.POST["bid_amt"])
        listing = Listing.objects.get(id=listing_id)
        
        if bid_amt > listing.start_bid and listing.user != request.user:
            new_bid = Bid(user = request.user, amount = bid_amt)
            new_bid.save()
            listing.start_bid = bid_amt
            listing.save()
        elif bid_amt <= listing.start_bid:
            messages.error(request, 'Bid must be greater than current high bid')

        return HttpResponseRedirect(reverse('get_listing', args=(listing_id,)))

@login_required
def closeBid(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        bidder = Bid.objects.get(amount=listing.start_bid)
        messages.success(request, f'{listing} sold to {bidder.user} for {bidder.amount}')
        #deactivate listing and label winner
        listing.winner = bidder
        listing.active = False
        listing.save()

        #remove item from watchlist if its in winners watchlist ( need to remove from all watchlists)
        
        if Watcher.objects.filter(user=bidder.user):
            watcher= Watcher.objects.get(user=bidder.user)
            selected = watcher.watchitems.get(id= listing_id)
            watcher.watchitems.remove(selected)

    
        return HttpResponseRedirect(reverse('get_listing', args=(listing_id,)))

@login_required
def makeComment(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        comment_content = request.POST["comment_content"]
        comment = Comment(user=request.user, listing=listing, content=comment_content)
        comment.save()
        return HttpResponseRedirect(reverse('get_listing', args=(listing_id,)))

