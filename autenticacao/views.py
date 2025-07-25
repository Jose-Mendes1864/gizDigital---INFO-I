from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.
# class moldeView(View):
#     def get(self,request, *args, **kwargs):
#         return HttpResponse('get')
#     def post(self,request, *args, **kwargs):
#         return HttpResponse('post')

class IndexView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'index.html')
    def post(self,request, *args, **kwargs):
        return HttpResponse('Teste')
    
class LoginView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'login.html')
    def post(self,request, *args, **kwargs):
        return HttpResponse('post')
    
class CadastrarView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'cadastro.html')
    def post(self,request, *args, **kwargs):
        return HttpResponse('post')