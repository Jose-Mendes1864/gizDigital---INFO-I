from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from autenticacao.models import PerguntaUsuario,Usuario,PerguntaDoQuestionario
from .models import Comunidade
from .functions import tiraCamelCase
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
            if kwargs.get('modificar_seguidor') != None:
                user = request.user
                c = Comunidade.objects.get(id=id_comunidade)
                if  c.membros.filter(id=user.id).exists():
                    c.membros.remove(user)
                else:
                    c.membros.add(user)

        else:
            carregar = 'posts'
        
        comunidade = Comunidade.objects.get(id=int(id_comunidade))
        user_joinded = Usuario.objects.filter(comunidades=comunidade.id, id=request.user.id).exists()
                # user .filter pois o .get não possui o método exists

        
       

        return render(request, 'comunidade.html', {'comunidade':comunidade,'carregar':carregar, 'user_joined':user_joinded})
    
class PerfilEdit(LoginRequiredMixin,View):


    template_name = "perfil.html"
    login_url = 'login'
     
    def get(self, request, *args, **kwargs):
        dados_usuario = {}
        try:
            
            for i in PerguntaDoQuestionario.objects.filter(aparecer_no_perfil=True):
              
                indice = i.titulo_pergunta
                indice = tiraCamelCase(indice)
                print(f'Valor do indive {indice}')
                dados_usuario[indice] = PerguntaUsuario.objects.get(user=request.user, pergunta=i).resposta
        except Exception as e:
            dados_usuario['i'] = 'Valor indefinido'
            print(f'Erro {e}')
        
        
                
        dados_usuario['Nome de usuario'] = request.user.username
        dados_usuario['date_joined'] = request.user.date_joined
        dados_usuario['Email'] = request.user.email 
        print(dados_usuario)
        print(dados_usuario)
        chaves_ordenadas = ['Biografia','Nome completo', 'Nome de usuario', 'Idade','Email', 'Area do saber', 'Anos experiencia',  'Material','Notificacoes', 'date_joined']
        dados_usuario_ordenado = {}
        
        try:
            for i in chaves_ordenadas:
                dados_usuario_ordenado[i] = dados_usuario[i]
        except Exception as e:
            print(f'Erro pois algum dado ali de chaves ordenadas não existe mais ou foi modificada erro: {e}')
        return render(request, self.template_name, {'user': request.user, 'dados_usuario': dados_usuario_ordenado}) 
    
