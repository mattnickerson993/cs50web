from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Follower
from .forms import PostForm
from django.db.models import Q
from functools import reduce
import json

from django.core.paginator import Paginator

def index(request):

    #handle pagination for all posts
    posts  = Post.objects.order_by('-date_created')
    #did not implement
    likes =[post.likers.filter(username=request.user) for post in posts]

    #pagination
    paginator = Paginator(posts, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #create new post
    if request.method == "POST":
        newPost = Post(user = request.user)
        form = PostForm(request.POST, instance = newPost)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": posts,
        'page_obj': page_obj,
        'likes': likes
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, username):

    #deals with follow button--- ie you cant follow yourself
    if username == str(request.user):
        usernamefollow = True
    else:
        usernamefollow = False

    #set initial display of follow btn to true
    displayfollowbtn= True
    
    
    # get the user object for username in url
    usersought= User.objects.get(username = username)

    #get all of this users posts and sort by date created
    posts = Post.objects.filter(user= usersought.id).order_by("-date_created")


    # handle pagination for users posts

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #count post and display number on page
    
    postCount = posts.count()

    
    
    

    if request.method == "POST":

        
        
        # handles a post request for the logged in user to follow a user who's page is displayed
        if request.POST["action"] == 'follow':
            usertoFollow = User.objects.get(username=username) 
            userthatwillfollow = request.user
            if not Follower.objects.filter(user=userthatwillfollow):
                newFollower = Follower(user= userthatwillfollow)
                newFollower.save()
                newFollower.following.add(usertoFollow)
            else:
                currentFollower = Follower.objects.get(user=userthatwillfollow)
                currentFollower.following.add(usertoFollow)
                currentFollower.save()
        
        # handle an unfollow request

        elif request.POST["action"] == 'unfollow':
            userToUnFollow = User.objects.get(username=username) 
            userThatWillUnfollow = request.user
                
            currentUnFollower = Follower.objects.get(user=userThatWillUnfollow)
            currentUnFollower.following.remove(userToUnFollow)
            currentUnFollower.save()

        # count number of users the user (who's page is displayed is following)
        followercount = Follower.objects.get(user=usersought)
        following = followercount.following.count()

        #count number of followers this user has 
        count = usersought.users_followers.all()

        
        # handle display of follow vs unfollow btn
        follower = Follower.objects.get(user = request.user)
        if follower.following.filter(username = username):
            displayfollowbtn = False

        return render(request, "network/profile.html", {
            "posts": posts,
            "postCount": postCount,
            "usernamefollow": usernamefollow,
            "username": username,
            "followers": len(count),
            "following": following,
            "displayfollowbtn": displayfollowbtn,
            "page_obj": page_obj
        })

    else:
        #handle scenario where user has not been a follower and needs to be created
        
        if not Follower.objects.filter(user=request.user):
            initFollower = Follower(user= request.user)
            initFollower.save()

        if not Follower.objects.filter(user=usersought):
            initFollower = Follower(user= usersought)
            initFollower.save()

        
        # count number of users this user is following
        followercount = Follower.objects.get(user=usersought)
        following = followercount.following.count()

        # count number of followers this user has
        count = usersought.users_followers.all()

        # handle display of follow vs unfollow btn
        follower = Follower.objects.get(user = request.user)
        if follower.following.filter(username = username):
            displayfollowbtn = False
        
        

        return render(request, "network/profile.html", {
            "posts": posts,
            "postCount": postCount,
            "usernamefollow": usernamefollow,
            "username": username,
            "followers": len(count),
            "following": following,
            "displayfollowbtn": displayfollowbtn,
            "page_obj": page_obj

        })

@login_required
def displayfollowing(request):

    # display posts from only the users the current logged in user is following, in chronological order
    if request.method == "GET":
        follower = Follower.objects.get(user = request.user)
        usersfollowed = follower.following.all()
        
                
        if usersfollowed:  
            posts = Post.objects.filter(reduce(lambda x,y : x | y, [Q(user=usr) for usr in usersfollowed])).order_by('-date_created')
            
        else:
            posts= ""

        # handle pagination of posts
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
        return render(request, "network/following.html", {
            "posts": posts,
            "page_obj": page_obj
        })

def edit_post(request, post_id):
    
    # provided data on post client is attempting to edit
    try: 
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(post.serialize())

@csrf_exempt
@login_required
def save_edited_post(request, post_id):

    # handle saving an edited post via PUT request from client
    try: 
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method =="PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required"
        }, status=400)

@csrf_exempt
@login_required
def manage_like(request, post_id):

    #handle addition or negation of like via API call from client
    try: 
        post = Post.objects.get(pk=post_id)
        
        if post.likers.filter(username=request.user):
            post.likers.remove(request.user)
        else:
            post.likers.add(request.user)
        post.save()

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # return to client
    if request.method == "GET":
        return JsonResponse(post.serialize())