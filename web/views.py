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





