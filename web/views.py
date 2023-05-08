from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.core.paginator import Paginator

import json

from django.http import JsonResponse

from .models import *


def change_like(request, post_id):
    current_post = Post.objects.get(pk=post_id)
    current_user = User.objects.get(pk=request.user.id)
    try:
        s = Like.objects.get(user=current_user, post=current_post)
        s.delete()
        current_post.number_of_likes -=1
        current_post.save()
        return JsonResponse({"message": "Like removed"})
    except:
        new_like = Like(user=current_user, post=current_post)
        new_like.save()
        current_post.number_of_likes +=1
        current_post.save()
        return JsonResponse({"message": "Like added"})
    
    

def index(request):
    allposts = Post.objects.all().order_by('id').reverse()
    current_user = request.user

    # Paginator
    paginator = Paginator(allposts, 10)
    page_namber = request.GET.get('page')
    page_obj = paginator.get_page(page_namber)

    return render(request, "web/index.html", {
                "allposts": page_obj,
                "current_user": current_user
            })

def post_edit(request, post_id):
    if request.method == "POST":
        post_body = json.loads(request.body)
        post = Post.objects.get(pk=post_id)
        post.content = post_body['content']
        post.save()
        return JsonResponse()
    

def userprofile(request):
    current_user = User.objects.get(id=request.user.id)
    allposts = Post.objects.filter(user=current_user).order_by('id').reverse()
    user_followers = current_user.number_of_followers
    user_following = current_user.number_of_following
    whoyoulike = []
    all_likes = Like.objects.all()
    for like in all_likes:
        if like.user == current_user:
            whoyoulike.append(like.post.id)

    # Paginator
    paginator = Paginator(allposts, 10)
    page_namber = request.GET.get('page')
    page_obj = paginator.get_page(page_namber)
    




    return render(request, "web/userprofile.html", {
                "allposts": page_obj,
                "current_user": current_user,
                "user_followers": user_followers,
                "user_following": user_following,
                "whoyoulike": whoyoulike
            })

def profileforuserid(request, post_user_id):
    current_user_id = request.user.id
    not_show_edit = True
    current_user1 = User.objects.get(id=request.user.id)
    if current_user_id == post_user_id:
        return HttpResponseRedirect(reverse('userprofile'))
    else:
        post_user = User.objects.get(id=post_user_id)

        user_followers = post_user.number_of_followers
        user_following = post_user.number_of_following 

        allposts = Post.objects.filter(user=post_user).order_by('id').reverse()
        allfollow = Follow.objects.all()
        current_following_postuser = False
        for item in allfollow:
            if item.follower == current_user1 and item.followed == post_user:
                current_following_postuser = True

        # Paginator
        paginator = Paginator(allposts, 10)
        page_namber = request.GET.get('page')
        page_obj = paginator.get_page(page_namber)        
        
        return render(request, "web/userprofile.html", {
                "allposts": page_obj,
                "current_user": post_user,
                "follow": current_following_postuser,
                "not_show_edit": not_show_edit,
                "user_followers": user_followers,
                "user_following": user_following
            })



def follow(request, post_user_id):
    if request.method == "POST":
        current_user = User.objects.get(id=request.user.id)
        post_user = User.objects.get(id=post_user_id)
        allposts = Post.objects.filter(user=post_user).order_by('id').reverse()
        new_follower = Follow(follower=current_user, followed=post_user)
        new_follower.save()
        current_user.number_of_following +=1
        current_user.save()
        post_user.number_of_followers +=1
        post_user.save()

        # Paginator
        paginator = Paginator(allposts, 10)
        page_namber = request.GET.get('page')
        page_obj = paginator.get_page(page_namber)

        user_followers = post_user.number_of_followers
        user_following = post_user.number_of_following 

        return render(request, "web/userprofile.html", {
                "allposts": page_obj,
                "current_user": post_user,
                "follow": True,
                "user_followers": user_followers,
                "user_following": user_following
            })


def unfollow(request, post_user_id):
    if request.method == "POST":
        current_user = User.objects.get(id=request.user.id)
        post_user = User.objects.get(id=post_user_id)
        allposts = Post.objects.filter(user=post_user).order_by('id').reverse()
        get_what_to_unfollow = Follow.objects.get(follower=current_user, followed=post_user)
        get_what_to_unfollow.delete()
        current_user.number_of_following -=1
        current_user.save()
        post_user.number_of_followers -=1
        post_user.save()

        # Paginator
        paginator = Paginator(allposts, 10)
        page_namber = request.GET.get('page')
        page_obj = paginator.get_page(page_namber)

        user_followers = post_user.number_of_followers
        user_following = post_user.number_of_following 

        return render(request, "web/userprofile.html", {
                "allposts": page_obj,
                "current_user": post_user,
                "follow": False,
                "user_followers": user_followers,
                "user_following": user_following
            })

def myfollowing(request):
    current_user = request.user
    followingpeople = Follow.objects.filter(follower=current_user)
    allposts = Post.objects.all().order_by('id').reverse()

    followingpost = []

    for post in allposts:
        for person in followingpeople:
            if person.followed == post.user:
                followingpost.append(post)

    # Paginator
    paginator = Paginator(followingpost, 10)
    page_namber = request.GET.get('page')
    page_obj = paginator.get_page(page_namber)            

    return render(request, "web/myfollowing.html", {
            "allposts": page_obj,
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





