from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
# Create your models here.


class Exercise(models.Model):
    title = models.CharField(max_length=80)
    description= models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default_exercise.png', upload_to='exercise_pics')
    

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse('exercise_detail', kwargs={'pk': self.pk})


class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    pic= models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"profile for {self.user.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pic.path)