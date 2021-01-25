from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Exercise, TrainingProgram, ExerciseStats
from django.contrib import messages
from .forms import RegisterNewUserForm, UserUpdateForm, ProfileUpdateForm
import os
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin

#Class based views

class ExerciseListView(ListView):
    model = Exercise
    template_name = "exercises/home.html"
    context_object_name ='exercises'
    ordering = ['-date_posted']
    paginate_by = 6

class TrainingProgramListView(ListView):
    model = TrainingProgram
    template_name = "exercises/training_programs.html"
    context_object_name ="training_programs"

    def get_queryset(self):
        return TrainingProgram.objects.filter(author= self.request.user)

class ExerciseDetailView(LoginRequiredMixin, DetailView):
    model = Exercise
   
class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ExerciseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# Create your views here.
    model= Exercise
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        exercise = self.get_object()
        if self.request.user == exercise.author:
            return True
        return False

class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    
    model = Exercise
    success_url = '/'

    def test_func(self):
        exercise = self.get_object()
        if self.request.user == exercise.author:
            return True
        return False

class TrainingProgramDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    
    model = TrainingProgram
    success_url = '/exercise/programs'
    success_message = "Training Program Successfully Deleted."

    def test_func(self):
        training_program = self.get_object()
        if self.request.user == training_program.author:
            return True
        return False
    
    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(TrainingProgramDeleteView, self).delete(request, *args, **kwargs)



class ProgramCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TrainingProgram
    fields = ['title']
    success_url= '/exercise/library'
    success_message = "Training Program successfully created. Select Exercises below"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ExerciseStatsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model=ExerciseStats
    success_url= '/exercise/programs'
    success_message = "Successfully removed from program"
    def test_func(self):
        exercise = self.get_object()
        if self.request.user == exercise.exerciser:
            return True
        return False
    
    def delete(self, request, *args, **kwargs):
        messages.error(self.request, self.success_message)
        return super(ExerciseStatsDeleteView, self).delete(request, *args, **kwargs)

class ExerciseStatsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# Create your views here.
    model= ExerciseStats
    fields = ['sets', 'reps', 'notes', 'time']
    success_url= '/exercise/programs'

    def form_valid(self, form):
        form.instance.exerciser = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        exercise = self.get_object()
        if self.request.user == exercise.exerciser:
            return True
        return False

def home(request):
    
    return render(request, "exercises/home.html", {
        "exercises": Exercise.objects.all()
    })

def register(request):
    # register user and redirect to login page
    if request.method == 'POST':
        form = RegisterNewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} successfully registered')
            return redirect('login')
    #otherwise display empty registration form
    else:
        form = RegisterNewUserForm()
    return render(request, "exercises/register.html",{
        'form': form
    }) 


@login_required
def profile(request):

    user = User.objects.get(username=request.user)
    #update profile via user and profile forms 
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.info(request, f'profile for {user.username} successfully updated')
            return redirect('profile')

    #otherwise display user and profile forms with info populated
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileUpdateForm(instance=user.profile)

    
    return render(request, "exercises/profile.html", {
        "user" : user,
        "user_form": user_form,
        "profile_form": profile_form
    } )

@login_required
def library(request):
    
    return render(request, "exercises/library.html")

@login_required
def retrieve_exercise_library(request, exercise_name):

    try:
        exercises = Exercise.objects.filter(title__startswith=exercise_name)
        
    except Exercise.DoesNotExist:
        return JsonResponse({"error": "Exercise not found"}, status= 404)

    if request.method == "GET":
        exercises = exercises.order_by("-date_posted").all()
        
        return JsonResponse([exercise.serialize() for exercise in exercises], safe=False)

@login_required
def retrieve_programs(request, pk):

    try: 
        program_list = list(TrainingProgram.objects.filter(author = request.user))
        program_list_copy = program_list.copy()
        for program in program_list_copy:
            for exStat in program.contents.all():
                if exStat.exercise.pk == pk:
                    program_list.remove(program)
        print(program_list)
    
    except TrainingProgram.DoesNotExist:
        return JsonResponse({"error": "Training programs not found"}, status= 404)
    
    if request.method == "GET":
        return JsonResponse([program.serialize() for program in program_list], safe=False)

@login_required
def save_to_program(request, pk, exid):
    try:
        program = TrainingProgram.objects.get(id=pk)
        added_exercise = Exercise.objects.get(id=exid)

        new_Ex= ExerciseStats(exercise=added_exercise, exerciser=request.user )
        new_Ex.save()
        program.contents.add(new_Ex)
        program.save()
        # messages.info(request, f'Exercise successfully added to training program')

    except TrainingProgram.DoesNotExist:
        return JsonResponse({"error": "Training program not found"}, status= 404)

    return JsonResponse({"message": "succesful"}, status=201)

@login_required
def display_program_exercises(request, pk):
    try: 
        program = TrainingProgram.objects.get(id = pk)
    
    except TrainingProgram.DoesNotExist:
        return JsonResponse({"error": "Training program not found"}, status= 404)
    
    if request.method == "GET":
        return JsonResponse(program.serialize())

@login_required
def programs(request):
    programs = TrainingProgram.objects.filter(author = request.user)
    for program in programs:
        for content in program.contents.all():
            print (content.exercise)

    return render(request, "exercises/programs.html", 
    {'programs': programs} )