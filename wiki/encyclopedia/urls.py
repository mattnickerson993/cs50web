from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.display_page, name="display_page")
]
