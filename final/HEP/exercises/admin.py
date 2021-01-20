from django.contrib import admin
from .models import Exercise, Profile, TrainingProgram, ExerciseStats
# Register your models here.

admin.site.register(Exercise)
admin.site.register(Profile)
admin.site.register(TrainingProgram)
admin.site.register(ExerciseStats)