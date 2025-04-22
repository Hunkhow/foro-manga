from django.urls import path
from .views import MangaListCreateAPI, MangaRetrieveUpdateDestroyAPI

urlpatterns = [
    path('mangas/', MangaListCreateAPI.as_view(), name='api-manga-list'),
    path('mangas/<int:pk>/', MangaRetrieveUpdateDestroyAPI.as_view(), name='api-manga-detail'),
]