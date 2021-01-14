from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Exercise
from django.contrib import messages
from .forms import RegisterNewUserForm, UserUpdateForm, ProfileUpdateForm
import os
from django.views.generic import ListView, DetailView, CreateView



#Class based views

class ExerciseListView(ListView):
    model = Exercise
    template_name = "exercises/home.html"
    context_object_name ='exercises'
    ordering = ['-date_posted']

class ExerciseDetailView(DetailView):
    model = Exercise
    
class ExerciseCreateView(CreateView):
    model = Exercise
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Create your views here.

def home(request):
    
    return render(request, "exercises/home.html", {
        "exercises": Exercise.objects.all()
    })

def register(request):
    if request.method == 'POST':
        form = RegisterNewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} successfully registered')
            return redirect('login')
    else:
        form = RegisterNewUserForm()
    return render(request, "exercises/register.html",{
        'form': form
    }) 


@login_required
def profile(request):

    user = User.objects.get(username=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.info(request, f'profile for {user.username} successfully updated')
            return redirect('profile')
    
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)

    
    return render(request, "exercises/profile.html", {
        "user" : user,
        "user_form": user_form,
        "profile_form": profile_form
    } )
