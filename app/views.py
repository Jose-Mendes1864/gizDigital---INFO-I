from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from autenticacao.models import PerguntaUsuario,Usuario,PerguntaDoQuestionario,PergutasCheckBox
from .models import Comunidade, Arquivo,Post,Reuniao
from autenticacao.models import Opcao,PerguntaDoQuestionario,Input
from .functions import tiraSnakeCase, pega_dados_comunidade, get_dados_input, adiciona_objetos_com_checkbox
import os
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django.contrib import auth
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
        else:
            carregar = 'posts'
        dados = pega_dados_comunidade(carregar, id_comunidade)
        
        comunidade = Comunidade.objects.get(id=int(id_comunidade))
        comunidade.posts= Post.objects.filter(id=int(id_comunidade))
        user_joinded = Usuario.objects.filter(comunidades=comunidade.id, id=request.user.id).exists()
                # user .filter pois o .get não possui o método exists

       
       

        return render(request, 'comunidade.html', {'comunidade':comunidade,'carregar':carregar, 'dados':dados ,'user_joined':user_joinded})
    def post(self, request,id_comunidade, *args, **kwargs): # nem tudo aqui é
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
        comunidade.posts= Post.objects.filter(id=int(id_comunidade))
        user_joinded = Usuario.objects.filter(comunidades=comunidade.id, id=request.user.id).exists()
                # user .filter pois o .get não possui o método exists

      
       

        return render(request, 'comunidade.html', {'comunidade':comunidade,'carregar':carregar, 'dados':dados ,'user_joined':user_joinded})

class EnviarComunidadeView(LoginRequiredMixin, View):
    def get(self, request, *args,**kwargs):
        pass
    def post(self, request,id_comunidade, carregar,  *args,**kwargs):
        if carregar == 'materiais':
            titulo = request.POST.get('titulo')
            material = request.FILES.get('material')
            descricao = request.POST.get('descricao')
            aux = material.name
            material.name = aux.replace(' ', '_')
           
            nome, ext = os.path.splitext(aux)

            a = Arquivo(
                usuario=request.user,
                comunidade= Comunidade.objects.get(id=id_comunidade),
                titulo=titulo,
                arquivo=material,
                descricao=descricao,
                ext = ext
            )
            a.save()
        elif carregar == 'eventos':
            titulo = request.POST.get('titulo')
            descricao = request.POST.get('descricao')
            url_da_reuniao = request.POST.get('url_da_reuniao')
            data = request.POST.get('data')
            hora = request.POST.get('hora')
            comunidade= Comunidade.objects.get(id=id_comunidade)
            user = request.user
            if data and hora:
                data_str = f"{data} {hora}"
                data_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M")
            if "https://meet.google.com/" in url_da_reuniao:
                evento = Reuniao(
                criador=user,
                comunidade=comunidade,
                tematica=titulo,
                descricao=descricao,
                url_da_reuniao=url_da_reuniao,
                data_hora=data_obj
            )
                evento.save()
            else:
                messages.add_message(request, constants.ERROR, "O lino fornecido é inválido" )
        return redirect('carregar', id_comunidade=id_comunidade,carregar=carregar)
            
        return HttpResponse('oi')

        




class PerfilEditView(LoginRequiredMixin,View):


    template_name = "perfil.html"
    login_url = 'login'
     
    def get(self, request, *args, **kwargs):
        dados_usuario = {}
        redefine_senha_status = request.GET.get('redefine_senha_status', None)# to passando essa variavel lá no refinir senha para ver se a senha digitada pel ousuario é a antiga mesmo
        try:
            
            for i in PerguntaDoQuestionario.objects.filter(aparecer_no_perfil=True):
                
                indice = i.titulo_pergunta
                indice = tiraSnakeCase(indice)
                if i.tipo_input.nome != 'checkbox':
                    dados_usuario[indice] = PerguntaUsuario.objects.get(user=request.user, pergunta=i).resposta
                else:
                    repostas_objects = PerguntaUsuario.objects.filter(user=request.user, pergunta=i)
                    lista = []
                    for i in repostas_objects:
                        lista.append(i.resposta)
                    dados_usuario[indice] = lista
                    
        except Exception as e:
            dados_usuario['i'] = 'Valor indefinido'
            print(f'Erro {e}')
        
        
                
        dados_usuario['Nome de usuario'] = request.user.username
        dados_usuario['date_joined'] = request.user.date_joined
        dados_usuario['Email'] = request.user.email 
        perguntas_com_check_box = PerguntaDoQuestionario.objects.filter(tipo_input__nome='checkbox')
        dados_usuario = adiciona_objetos_com_checkbox(request,perguntas_com_check_box,dados_usuario)
    
        chaves_ordenadas = ['Biografia','Nome completo', 'Nome de usuario', 'Idade','Email', 'Area do saber', 'Anos de experiencia',  'Material','Notificacoes', 'Para quem leciona','date_joined']
        dados_usuario_ordenado = {}
        
        try:
           for i in chaves_ordenadas:
            dados_usuario_ordenado[i] = dados_usuario[i]
        
        except Exception as e:
            print(f'Erro pois algum dado ali de chaves ordenadas não existe mais ou foi modificada erro: {e}')
        dados_com_select = get_dados_input('select')
        dados_com_checkbox = get_dados_input('checkbox')
    
        return render(request, self.template_name, {'user': request.user, 'dados_com_select':dados_com_select,  'dados_com_checkbox': dados_com_checkbox,'dados_usuario': dados_usuario_ordenado, 'redefine_senha_status':redefine_senha_status}) 
    def post(self, request, *args, **kwargs):
        return HttpResponse('Em processo')
class VerPerfilView(LoginRequiredMixin, View):
    def get(self, request, id,*args, **kwargs):
        return HttpResponse(f'Ver pefil {id}')
    def post(self, request, id,*args, **kwargs):
        pass
class ModificarPerfilView(LoginRequiredMixin, View):
    def get(self, request, id,*args, **kwargs):
       pass
    def post(self, request, id,*args, **kwargs):
        dados = dict(request.POST.copy())
        # como checkbox se seleiconar nada não vem nada preciso passar pelas perguntas com checkbox a parte
        dados_sem_csrf = {}
        if request.FILES.get('foto'):
            dados['foto'] = [request.FILES.get('foto')]

        cont = 0
        for i,j in dados.items():
            if cont == 0:
                cont+=1
                continue
            if i == 'nome_de_usuario':

                dados_sem_csrf['username'] = j
                continue
            dados_sem_csrf[i] = j
            
        dados = dados_sem_csrf
        for nome_campo,value in dados.items():
             nome_campo =nome_campo.lower()
             campo_in_questionario = PerguntaUsuario.objects.filter(user=request.user, pergunta__titulo_pergunta=nome_campo)
             campo_in_checkbox = PergutasCheckBox.objects.filter(usuario=request.user,opcao__pergunta__titulo_pergunta=nome_campo)
         
             if campo_in_questionario or campo_in_checkbox:
                 print(f'teste{len(campo_in_questionario)} e campo checkcbox {campo_in_checkbox}')
                 if len(campo_in_questionario) == 1:
                    instancia = campo_in_questionario.first()
                   
                      
                    setattr(instancia, 'resposta' ,value[0])
                    instancia.save()
                 else: # quer dizer que campo in questionario não retonrou nada
                    pergunta = PerguntaDoQuestionario.objects.get(titulo_pergunta=nome_campo)
                    opcoes = []
                    opcoes.append(PergutasCheckBox.objects.filter(opcao__pergunta=pergunta)) # pega os valroes selecionados pelo usuario com a pergunta

                    for i in opcoes:
                        i.delete()
                    print(f'Valor de value {value}')
                    for i in value:
                        op = Opcao.objects.get(nome=i, pergunta__titulo_pergunta=nome_campo)
                        p = PergutasCheckBox(
                            opcao=op,
                            usuario=request.user

                        ) 
                        p.save()


                    
                    
                    
             else:# ou seja  a pergunta esta na tabela usuarios mesmo
                user = request.user
                if(nome_campo == 'username' or nome_campo == 'email'):
                    dicti = {nome_campo : value[0]}
                    if Usuario.objects.filter(**dicti):
                        if nome_campo == 'username':
                            nome_campo = 'Nome do usuario'
                        messages.add_message(request, constants.WARNING, f'O campo {tiraSnakeCase(nome_campo)} já esta sendo utilizado por outro usuario')
                        
                    else:
                        
                        setattr(user, nome_campo, value[0])

                else:
                    setattr(user, nome_campo, value[0])
             
                user.save()
        return redirect('perfil')
       
        return HttpResponse(dados)

class RedefineSenhaView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        senha_atual = request.POST.get('senha_atual', None)
        if senha_atual: #  pra ver se a senha atual foi digitada  coretamente
            if check_password(senha_atual,request.user.password):
                url = reverse('perfil')
                return redirect(f'{url}?redefine_senha_status=True')
            else:   
                messages.add_message(request, constants.ERROR, 'Senha incorreta')
                return redirect('perfil')
    
        else: # ai já ta no redefinir senha, pois a senha atual já foi acertada
            senha  =request.POST.get('senha')
            user = request.user
            user.set_password(senha)
            user.save()
            # Mantém o usuário logado após mudar a senha
            auth.update_session_auth_hash(request, user)

            messages.add_message(request, constants.SUCCESS, "Senha redefinida com sucesso")
            return redirect('Perfil')