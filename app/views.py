from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexComunidadeView(LoginRequiredMixin,View):
    template_name = "indexComunidade.html"
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        return render(request, 'indexComunidade.html')
      

class ComunidadeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'comuBase.html')
    
class PerfilEdit(LoginRequiredMixin,View):
    template_name = "perfil.html"
    login_url = 'login'
     
    def get(self, request, *args, **kwargs):
        print(request.user.username)
        return render(request, self.template_name, {'user': request.user}) 