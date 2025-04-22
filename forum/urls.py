from django.urls import path
from .views import (
    ThreadListView, ThreadDetailView,
    ThreadCreateView, ThreadUpdateView, ThreadDeleteView,
    PostCreateView, PostUpdateView, PostDeleteView,
    post_upvote_toggle, AnimeGenreListView,AnimeListByGenreView
)

app_name = 'forum'

urlpatterns = [
    # 1) Listado
    path('', ThreadListView.as_view(), name='thread-list'),

    # 2) Crear hilo (ESTÁTICA)
    path('thread/create/', ThreadCreateView.as_view(), name='thread-create'),

    # 3) Editar y borrar hilo (ESTÁTICAS también)
    path('thread/<slug:slug>/edit/',   ThreadUpdateView.as_view(), name='thread-edit'),
    path('thread/<slug:slug>/delete/', ThreadDeleteView.as_view(), name='thread-delete'),

    # 4) Detalle de hilo (VARIABLE)
    path('thread/<slug:slug>/', ThreadDetailView.as_view(), name='thread-detail'),

    # 5) Responder al hilo
    path('thread/<slug:slug>/reply/', PostCreateView.as_view(), name='post-reply'),

    # 6) Editar/borrar respuesta (post)
    path('post/<int:pk>/edit/',   PostUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # 7) Upvote toggle
    path('post/<int:pk>/upvote/', post_upvote_toggle, name='post-upvote'),
    path('anime/genres/', AnimeGenreListView.as_view(), name='anime-genre-list'),

    # Listado de animes por género
    path(
      'anime/genre/<int:genre_id>/',
      AnimeListByGenreView.as_view(),
      name='anime-by-genre'
    ),
]