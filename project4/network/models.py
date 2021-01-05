from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "posts")
    content = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post created by {self.user} on {self.date_created}"

    def serialize(self):
        return {
            "user": self.user.username,
            "content": self.content,
            "date_created": self.date_created
        }
        
class Follower(models.Model):
    user =models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    following = models.ManyToManyField(User, blank=True, related_name="users_followers")

    def __str__(self):
        return f"{self.user} is a follower"