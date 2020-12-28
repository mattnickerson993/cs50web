from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.get_listing, name="get_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("makeBid/<int:listing_id>", views.makeBid, name="makeBid"),
    path("closeBid/<int:listing_id>", views.closeBid, name="closeBid"),
    path("makeComment/<int:listing_id>", views.makeComment, name="makeComment"),
    path("get_category", views.get_category, name="get_category")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)