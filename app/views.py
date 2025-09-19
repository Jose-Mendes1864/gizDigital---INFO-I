from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from autenticacao.models import PerguntaUsuario,Usuario,PerguntaDoQuestionario,MaterialUsuarios
from .models import Comunidade, Arquivo
from .functions import tiraCamelCase, pega_dados_comunidade
import os
# Create your views here.

class IndexComunidadeView(LoginRequiredMixin,View):
    template_name = "indexComunidade.html"
    login_url = 'login'
    def get(self, request, *args, **kwargs):
        comunidades = Comunidade.objects.all()
        
        return render(request, 'indexComunidade.html', {'comunidades':comunidades })
    
      

class ComunidadeView(LoginRequiredMixin,View):
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
        dados = pega_dados_comunidade(carregar, id_comunidade)
        
        comunidade = Comunidade.objects.get(id=int(id_comunidade))
        user_joinded = Usuario.objects.filter(comunidades=comunidade.id, id=request.user.id).exists()
                # user .filter pois o .get não possui o método exists

       
       

        return render(request, 'comunidade.html', {'comunidade':comunidade,'carregar':carregar, 'dados':dados ,'user_joined':user_joinded})

class EnviarComunidadeView(LoginRequiredMixin, View):
    def get(self, request, *args,**kwargs):
        pass
    def post(self, request,id_comunidade, carregar,  *args,**kwargs):
        if carregar == 'materiais':
            titulo = request.POST.get('titulo')
            material = request.POST.get('material')
            descricao = request.POST.get('descricao')
            material = material.replace(' ', '_')
            nome, ext = os.path.splitext(material)
            a = Arquivo(
                usuario=request.user,
                comunidade= Comunidade.objects.get(id=id_comunidade),
                titulo=titulo,
                arquivo=material,
                descricao=descricao,
                ext = ext
            )
            a.save()
            return redirect('carregar', id_comunidade=id_comunidade,carregar=carregar)
        
        return HttpResponse('oi')

        




class PerfilEditView(LoginRequiredMixin,View):


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
        objects_materiais = MaterialUsuarios.objects.filter(usuario=request.user)
        lista_material = []
        for o in objects_materiais:
            lista_material.append(o.opcao)

        dados_usuario['materiais'] = lista_material
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
    
class VerPerfilView(LoginRequiredMixin, View):
    def get(self, request, id,*args, **kwargs):
        return HttpResponse(f'Ver pefil {id}')
    def post(self, request, id,*args, **kwargs):
        pass