from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from autenticacao.models import PerguntaUsuario
from .models import Comunidade
# Create your views here.

class IndexComunidadeView(LoginRequiredMixin,View):
    template_name = "indexComunidade.html"
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        comunidades = Comunidade.objects.all()
        
        return render(request, 'indexComunidade.html', {'comunidades':comunidades })
    
      

class ComunidadeView(View):
    def get(self, request,id_comunidade, *args, **kwargs):
        if kwargs:
            carregar = kwargs.get('carregar', 'nada')

        else:
            carregar = 'posts'
        
        comunidade = Comunidade.objects.get(id=int(id_comunidade))
        print(comunidade)

        return render(request, 'comunidade.html', {'comunidade':comunidade,'carregar':carregar})
    
class PerfilEdit(LoginRequiredMixin,View):
    template_name = "perfil.html"
    login_url = 'login'
     
    def get(self, request, *args, **kwargs):
        try:
            dados_pesquisa  = PerguntaUsuario.objects.get(user=request.user.id)
        except:
            dados_pesquisa = ['Dados não encontrados',]

        return render(request, self.template_name, {'user': request.user, 'dados_pesquisa': dados_pesquisa}) 