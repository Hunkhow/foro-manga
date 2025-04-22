from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from forum.models import Manga
from forum.serializers import MangaSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class MangaListCreateAPI(generics.ListCreateAPIView):
    queryset = Manga.objects.all().order_by('-created_at')
    serializer_class = MangaSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

 

class MangaRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manga.objects.all()
    serializer_class = MangaSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated] 


    
class CustomAuthToken(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(
            data = request.data,
            context = {'request':request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token,created = Token.objects.get_or_create(user=user)

        return Response({'token':token.key})