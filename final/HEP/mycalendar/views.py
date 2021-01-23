from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.apps import apps
import os
import pytz
from tzlocal import get_localzone


# Create your views here.

@login_required
def index(request):
    
    

    local_tz = get_localzone()
    
    TrainingProgram = apps.get_model('exercises', 'TrainingProgram')
    
    return render(request, "mycalendar/index.html",{
        "programs": TrainingProgram.objects.filter(author= request.user),
        "apiKey": os.environ.get("CALENDAR_API_KEY"),
        "clientID": os.environ.get("CALENDAR_CLIENT_ID"),
        "timezone": local_tz
    })