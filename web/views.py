from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError

from .models import *


def index(request):
    allposts = Post.objects.all().order_by('id').reverse()
    current_user = request.user

    return render(request, "web/index.html", {
                "allposts": allposts,
                "current_user": current_user
            })


def userprofile(request):
    current_user = request.user
    allposts = Post.objects.filter(user=current_user)



    return render(request, "web/userprofile.html", {
                "allposts": allposts,
                "current_user": current_user
            })

def profileforuserid(request, post_user_id):
    current_user_id = request.user.id
    current_user1 = User.objects.get(id=request.user.id)
    if current_user_id == post_user_id:
        return HttpResponseRedirect(reverse('userprofile'))
    else:
        post_user = User.objects.get(id=post_user_id)
        allposts = Post.objects.filter(user=post_user)
        allfollow = Follow.objects.all()
        current_following_postuser = False
        for item in allfollow:
            if item.follower == current_user1 and item.followed == post_user:
                current_following_postuser = True
        
        return render(request, "web/userprofile.html", {
                "allposts": allposts,
                "current_user": post_user,
                "follow": current_following_postuser
            })



def follow(request, post_user_id):
    if request.method == "POST":
        current_user = User.objects.get(id=request.user.id)
        post_user = User.objects.get(id=post_user_id)
        allposts = Post.objects.filter(user=post_user)
        new_follower = Follow(follower=current_user, followed=post_user)
        new_follower.save()
        return render(request, "web/userprofile.html", {
                "allposts": allposts,
                "current_user": post_user,
                "follow": True
            })


def unfollow(request, post_user_id):
    if request.method == "POST":
        current_user = User.objects.get(id=request.user.id)
        post_user = User.objects.get(id=post_user_id)
        allposts = Post.objects.filter(user=post_user)
        get_what_to_unfollow = Follow.objects.get(follower=current_user, followed=post_user)
        get_what_to_unfollow.delete()
        return render(request, "web/userprofile.html", {
                "allposts": allposts,
                "current_user": post_user,
                "follow": False
            })



def newpost(request):
    if request.method == "POST":
        user = request.user
        content = request.POST['content']
        newpost = Post(user=user, content=content)
        newpost.save()
        return HttpResponseRedirect(reverse('index'))

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        # Check if Successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "web/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "web/login.html")    


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords are same
        if password != confirm_password:
            return render(request, "web/register.html", {
                "message": "Passwords must match."
            })
        
        else:
            # Create a new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                return render(request, "network/register.html", {
                "message": "Username already taken."
            })
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "web/register.html")





