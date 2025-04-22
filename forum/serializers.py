from rest_framework import serializers
from .models import Manga

class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = ['id', 'title', 'slug', 'description', 'cover_image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']