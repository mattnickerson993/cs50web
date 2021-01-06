
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.displayfollowing, name="following"),
    path("<str:username>", views.profile, name="profile"),

    # API ROUTES

    path("posts/edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("posts/save/<int:post_id>", views.save_edited_post, name="save_edited_post"),
    path("posts/like/<int:post_id>", views.manage_like, name="manage_like")

    
    
]
