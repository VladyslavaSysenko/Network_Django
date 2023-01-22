from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

from .models import User, Post, Like, Following


def start(request):
    return HttpResponseRedirect(reverse("index", kwargs={'page':1}))


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index", kwargs={'page':1}))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index", kwargs={'page':1}))


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
        return HttpResponseRedirect(reverse("index", kwargs={'page':1}))
    else:
        return render(request, "network/register.html")


def paginator(posts, page):
    # paginate posts
    paginator = Paginator(posts, per_page=10)
    # choose needed posts for page
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=1, on_ends=0)
    return page_object


def index(request, page):
    posts = Post.objects.all().order_by("-id")
    return render(request, "network/index.html",{
        "posts": paginator(posts, page),
        "way": "index"
    })


@login_required
def new_post(request):
    if request.method == "PUT":
        #check if not empty
        text = json.loads(request.body).get("text")
        if text != "":
            # Make new post
            new = Post(
                user = request.user,
                text = text
            )
            new.save()
            return JsonResponse({"success": "yes"})
        else:
            return JsonResponse({"success": "no"})


@login_required
def following_posts(request, page):
    # Open page with posts of following accounts
    user = User.objects.get(id=request.user.id)
    following = list(user.following.values_list('following', flat=True))
    posts = Post.objects.filter( user__in = following).order_by("-id")
    return render(request, "network/index.html",{
        "posts": paginator(posts, page),
        "way": "following_posts"
    })


def user_page(request, username, page):
    # follow or unfollow
    if request.method == "PUT":
        user = User.objects.get(id=request.user.id)
        userpage = User.objects.get(username=username)
        # Unfollow if user follows userpage
        try:
            user.following.get(following=userpage).delete()
        # Follow if user doesn't follow userpage
        except Following.DoesNotExist:
            Following(follower=user, following=userpage).save()
        return JsonResponse({"success": "yes"})
    # Open user page
    else:
        posts = Post.objects.filter(user = User.objects.get(username=username)).order_by("-id")
        return render(request, "network/index.html",{
            "userpage":User.objects.get(username=username),
            "posts": paginator(posts, page),
            "way": "user_page"
        })


def follow_info(request, username):
    # Return info about followers and followings 
    if request.method == "PUT":
        user = request.user
        userpage = User.objects.get(username=username)
        if request.user.is_authenticated:
            un_followed = user.following.filter(following=userpage).count()
        else:
            un_followed = "anonymous"
        return JsonResponse({
            "followers":userpage.followers.count(),
            "following":userpage.following.count(),
            "un_followed":un_followed})


def like(request, post_id):
    # Like or unlike
    if request.method == "PUT":
        user = User.objects.get(id=request.user.id)
        # Unlike
        try:
            user.like.get(post__id=post_id).delete()
        # Like
        except Like.DoesNotExist:
            Like(user=user, post=Post.objects.get(id=post_id)).save()
        return JsonResponse({"success": "yes"})


def like_info(request, post_id):
    # Return info about likes
    if request.method == "PUT":
        try:
            user = User.objects.get(id=request.user.id)
            return JsonResponse({
                "amount_likes":Like.objects.filter(post__id=post_id).count(),
                "un_liked":Like.objects.filter(user=user, post__id=post_id).count()})
        except User.DoesNotExist:
            return JsonResponse({
                "amount_likes":Like.objects.filter(post__id=post_id).count()})


def edit(request, post_id):
    # edit post
    post = Post.objects.get(id=post_id)
    if request.user == post.user:
        if request.method == "PUT":
            text = json.loads(request.body).get("text")
            post = Post.objects.get(id=post_id)
            post.text = text
            post.save()
            return JsonResponse({"success": "yes"})


