from django.urls import  path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("userprofile", views.userprofile, name="userprofile"),
    path("profileforuserid/<int:post_user_id>", views.profileforuserid, name="profileforuserid"),
    path("follow/<int:post_user_id>", views.follow, name="follow"),
    path("unfollow/<int:post_user_id>", views.unfollow, name="unfollow"),
    path("myfollowing", views.myfollowing, name="myfollowing"),
    path("post_edit/<int:post_id>", views.post_edit, name="post_edit"),
    path("change_like/<int:post_id>", views.change_like, name="change_like"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),
    
  
    


]