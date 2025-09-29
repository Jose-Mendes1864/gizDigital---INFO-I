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
from .views import  IndexComunidadeView, ComunidadeView, PerfilEditView,EnviarComunidadeView,VerPerfilView,ModificarPerfilView,RedefineSenhaView
urlpatterns = [
    path('', IndexComunidadeView.as_view(), name='indexComunidade'),
    path('comunidade/<int:id_comunidade>/', ComunidadeView.as_view(), name='comunidade'),
    path('comunidade/<int:id_comunidade>/<str:carregar>/', ComunidadeView.as_view(), name='carregar'),
    path('comunidade/enviar_arquivo/ <int:id_comunidade>/<str:carregar>/', EnviarComunidadeView.as_view(), name='enviar_comunidade'),

    path('comunidade/<int:id_comunidade>/<str:carregar>/<str:modificar_seguidor>', ComunidadeView.as_view(), name='modifica_joined'),
    path('perfil/', PerfilEditView.as_view(), name='perfil'),
    path('perfil/reset_password', RedefineSenhaView.as_view(), name='redefine_senha') ,

    path('perfil/ver_perfil/<int:id>', VerPerfilView.as_view(), name='view_profile' ),
    path('perfil/modificar_perfil', ModificarPerfilView.as_view(), name='modify_profile' )

    
]
