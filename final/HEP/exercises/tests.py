from django.test import TestCase
from .models import Exercise, ExerciseStats
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your tests here.
class ExerciseModelTests(TestCase):

    def setUp(self):
        
        user1 = User.objects.create(username="matt", password="password123")
        user2 = User.objects.create(username="nick", password="password1234")
        e1 = Exercise.objects.create(title = "lunge", author= user1, description = "lunge exercise")
        e2 = Exercise.objects.create(title="pull up", author=user2, description="lat exercise")
        ExerciseStats.objects.create(exercise=e1, exerciser=user2)


    

    def testEx(self):
        e = Exercise.objects.get(title = "lunge")
        self.assertEqual(e.title, "lunge")
    
    
    def testDateWorking(self):
        current_year = timezone.now().year
        ex_date = Exercise.objects.filter(date_posted__year= current_year).count()
        self.assertIs(ex_date, 2)
    
    def testCount(self):
        total = Exercise.objects.all().count()
        self.assertEqual(int(total), 2)


    def testExStat(self):
        stat = ExerciseStats.objects.all().first()
        self.assertEqual(stat.reps, 10)


