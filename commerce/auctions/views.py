from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(label="Description", max_length=255, widget=forms.Textarea(attrs={'class':'form-control'}))
    active = forms.BooleanField(required = True,)
    start_bid = forms.DecimalField(label="Starting Bid", max_digits=10, decimal_places=2)
    category = forms.CharField(label="Category", max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    # date = forms.DateTimeField(label="Date and Time")




def index(request):
    if request.method == "GET":
        return render(request, "auctions/index.html", {
            "listings" : Listing.objects.all()
        })


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

def create_listing(request):
    if request.method == 'GET':
        form = NewListingForm()
        print(form)
        return render(request, "auctions/create.html", {
            "form": form
        })
    if request.method == 'POST':
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            active = form.cleaned_data["active"]
            start_bid = form.cleaned_data["start_bid"]
            # date = form.cleaned_data["date"]
            listing = Listing(title= title, description= description, category= category, active= active, start_bid= start_bid)
            listing.save()
            return render(request, "auctions/index.html")
