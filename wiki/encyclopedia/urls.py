from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.display_page, name="display_page"),
    path("navbar/search", views.search, name="search"),
    path("navbar/newpage", views.new_page, name="new_page"),
    path("navbar/editcontent/<str:title>", views.edit_content, name="edit_content" ),
    path("navbar/random", views.random_page, name="random")
]
