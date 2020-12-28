from django.contrib.auth.models import AbstractUser
from django.db import models


CATEGORIES =(
    ('fitness', 'FITNESS'),
    ('electric', 'ELECTRIC'),
    ('outdoor', 'OUTDOOR'),
    ('sports', 'SPORTS'),
    ('cosmetic', 'COSMETIC'),
    ('kitchen', 'KITCHEN'),
    ('grocery', 'GROCERY'),
    ('other', 'OTHER'),
)
class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE, related_name = "bids")
    amount = models.DecimalField(max_digits=10, decimal_places = 2)

    def __str__(self):
        return f"bid of {self.amount} by {self.user}"
        
class Listing(models.Model):
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE, related_name = "listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    # date = models.DateTimeField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="", null=True, blank=True)
    winner = models.ForeignKey(Bid, null=True, blank=True, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='images/', default ="default.jpg", blank = True)
    #need to do image url

    def __str__(self):
        return f"{self.title} listed by {self.user}"

class Watcher(models.Model):
    user = models.OneToOneField(User, on_delete= models.PROTECT)
    watchitems = models.ManyToManyField(Listing, blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.user} has the following {self.watchitems.all()}"


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return f"{self.content} by {self.user} on {self.listing}"