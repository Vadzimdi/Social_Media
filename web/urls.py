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
    path("myfollowing", views.myfollowing, name="myfollowing")

]