from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    content = models.CharField(max_length=140)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    number_of_likes = models.IntegerField(default=0)
    comments = models.ManyToManyField('Comments', blank=True, related_name="comments")

    def __str__(self):
        return f'{self.user} write a post {self.content}'
    

class Comments(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")


    
