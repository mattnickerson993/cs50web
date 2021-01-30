from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import TrainingProgramDeleteView, TrainingProgramListView, ExerciseStatsUpdateView, ExerciseStatsDeleteView, ExerciseListView, ExerciseDetailView, ExerciseCreateView, ExerciseUpdateView, ExerciseDeleteView, ProgramCreateView

urlpatterns = [
    path('', ExerciseListView.as_view(), name="exercises-home"),
    path('exercise/training_programs', TrainingProgramListView.as_view(), name="training_programs_list"),
    path('exercise/<int:pk>/', ExerciseDetailView.as_view(), name="exercise_detail"),
    path('exercise/create', ExerciseCreateView.as_view(), name="exercise_create"),
    path('exercise/update/<int:pk>', ExerciseUpdateView.as_view(), name="exercise_update"),
    path('exercise/delete/<int:pk>', ExerciseDeleteView.as_view(), name="exercise_delete"),
    path('exercise/trainingprogram/delete/<int:pk>', TrainingProgramDeleteView.as_view(), name="training_program_delete"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="exercises/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="exercises/logout.html"), name="logout"),
    path('profile/', views.profile, name="profile"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="exercises/password_reset.html"), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="exercises/password_reset_done.html"), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="exercises/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="exercises/password_reset_complete.html"), name="password_reset_complete"),
    path('exercise/library', views.library, name='library'),
    path('exercise/programs', views.programs, name="programs"),
    path('exercise/programs/create', ProgramCreateView.as_view(), name="create_program"),
    path('exercise/exercisestats/delete/<int:pk>/', ExerciseStatsDeleteView.as_view(), name="exercisestats_delete"),
    path('exercise/exercisestats/update/<int:pk>/', ExerciseStatsUpdateView.as_view(), name="exercisestats_update"),
    path('myHEP', views.myHEP, name="myHEP"),


    #API ROUTES
    path('exercise/library/retrieve/<str:exercise_name>', views.retrieve_exercise_library, name="retrieve_exercise_library"),
    path('exercise/add/<int:pk>', views.retrieve_programs, name="retrieve_programs"),
    path('exercise/add/save/<str:pk>/<str:exid>', views.save_to_program, name="save_to_program"),
    path('exercise/programs/retrieve/<str:pk>', views.display_program_exercises, name="display_program_exercises")
]
