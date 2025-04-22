from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from forum.models import Manga
from forum.serializers import MangaSerializer

class MangaListCreateAPI(generics.ListCreateAPIView):
    queryset = Manga.objects.all().order_by('-created_at')
    serializer_class = MangaSerializer
    permission_classes = [AllowAny]  

class MangaRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manga.objects.all()
    serializer_class = MangaSerializer
    permission_classes = [AllowAny] 