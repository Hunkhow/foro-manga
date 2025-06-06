"""
URL configuration for foromanga project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from forum.views import HomeView

urlpatterns = [
    # Home
    path('', HomeView.as_view(), name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # Foro
    path('forum/', include(('forum.urls', 'forum'), namespace='forum')),

    # Autenticación (login, logout, cambio de pass…) 
    path('accounts/', include('django.contrib.auth.urls')),

    # Registro y perfil (signup, profile_detail, profile_edit, account_delete…)
    path('accounts/', include(('users.urls', 'users'), namespace='users')),
    
    # API path
    path('api/', include(('forum.api.urls', 'forum.api'), namespace='forum-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)