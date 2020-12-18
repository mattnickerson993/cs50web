from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<title>", views.display_page, name="display_page")
]
