from django.shortcuts import render,redirect
from django.contrib import auth
def sair(request):
    auth.logout(request)
    return redirect('login')