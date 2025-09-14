"""
URL configuration for config project.

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
from django.contrib import admin
from django.urls import path
from  django.shortcuts import redirect
from .views import  IndexComunidadeView, ComunidadeView, PerfilEdit
urlpatterns = [
    path('', IndexComunidadeView.as_view(), name='indexComunidade'),
    path('comunidade/<int:id_comunidade>/', ComunidadeView.as_view(), name='comunidade'),
    path('comunidade/<int:id_comunidade>/<str:carregar>/', ComunidadeView.as_view(), name='carregar'),
    path('perfil/', PerfilEdit.as_view(), name='perfil'),
    
    
]
