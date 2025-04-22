from django.urls import path
from .views import MangaListCreateAPI, MangaRetrieveUpdateDestroyAPI,CustomAuthToken

urlpatterns = [
    path('mangas/', MangaListCreateAPI.as_view(), name='api-manga-list'),
    path('mangas/<int:pk>/', MangaRetrieveUpdateDestroyAPI.as_view(), name='api-manga-detail'),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth')
]