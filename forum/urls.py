from django.urls import path
from .views import (
    ThreadListView, ThreadDetailView,
    ThreadCreateView, PostCreateView,
    post_upvote_toggle
)

app_name = 'forum'

urlpatterns = [
    path('',                       ThreadListView.as_view(),   name='thread-list'),
    path('thread/create/',         ThreadCreateView.as_view(), name='thread-create'),
    path('thread/<slug:slug>/',    ThreadDetailView.as_view(), name='thread-detail'),
    path('thread/<slug:slug>/reply/', PostCreateView.as_view(),  name='post-reply'),
    path('post/<int:pk>/upvote/', post_upvote_toggle, name='post-upvote')
]