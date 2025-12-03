
from django.contrib import admin
from django.urls import path
from  django.shortcuts import redirect
from .views import *
urlpatterns = [
    path('', SuporteView.as_view(), name='suporte'),

    
]
