from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_anime, name="home"),
    path("anime-info/<int:anime_id>/", views.get_anime_info, name="anime-info"),
]
