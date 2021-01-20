from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from datetime import timedelta
# Create your models here.


class Exercise(models.Model):
    title = models.CharField(max_length=80)
    description= models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image= models.ImageField(default='default_exercise.png', upload_to='exercise_pics')
    

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('exercise_detail', kwargs={'pk': self.pk})
    
    def serialize(self):
        return {
            "title": self.title,
            "description": self.description,
            "date_posted": self.date_posted,
            "author":self.author.username,
            "image": self.image.url,
            "author_pic":self.author.profile.pic.url,
            "id":self.id

        }


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

class ExerciseStats(models.Model):
    exerciser = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="stats")
    sets = models.PositiveIntegerField(blank=True, default=3)
    reps = models.PositiveIntegerField(blank=True, default=10)
    notes = models.TextField(blank=True)
    time = models.DurationField(blank=True, default=timedelta(minutes=0, seconds=0))
    

    def __str__(self):
        return f"{self.exerciser} will perform {self.exercise} for {self.sets} sets of {self.reps} reps"

class TrainingProgram(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    contents = models.ManyToManyField(ExerciseStats)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def serialize(self):
        return {
            "title": self.title,
            "contents": [exercise_stats.exercise.title for exercise_stats in self.contents.all()],
            "id":self.pk

        }





