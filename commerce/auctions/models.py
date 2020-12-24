from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE, related_name = "listings")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    # date = models.DateTimeField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField( default="images/default.jpg", upload_to="images/", blank = True)
    #need to do image url

    def __str__(self):
        return f"{self.title} listed by {self.user}"

class Watcher(models.Model):
    user = models.OneToOneField(User, on_delete= models.PROTECT)
    watchitems = models.ManyToManyField(Listing, blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.user} has the following {self.watchitems}"