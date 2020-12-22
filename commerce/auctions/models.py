from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    # date = models.DateTimeField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20)
    #need to do image url