from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

from .models import  Usuario,PerguntaDoQuestionario,Opcao,PergutasCheckBox, PerguntaUsuario,Input
from .functions import enviar_email_async
import secrets
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

# Create your views here.
# class moldeView(View):
#     def get(self,request, *args, **kwargs):
#         return HttpResponse('get')
#     def post(self,request, *args, **kwargs):
#         return HttpResponse('post')

class IndexView(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('indexComunidade')
        return render(request, 'index.html')
    def post(self,request, *args, **kwargs):
        
        return HttpResponse('Teste')
    
class LoginView(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            # combina a pesquisa + o request .user
            if request.user.is_staff == 1:
                return redirect(reverse('admin:index')) #reverse retorna a url de index:admin
            return redirect('indexComunidade')


        return render(request, 'login.html')
    def post(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff == 1:
                return redirect(reverse('admin:index'))
            return redirect('indexComunidade')
 
        email = request.POST.get('email').strip()
        senha = request.POST.get('senha')
       
        usuario = auth.authenticate(request, username=email, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Por favor insira email e senha corretos')
            return redirect('login')
        else:  
            
                
            auth.login(request, usuario) 
            if request.user.is_staff == 1:
                return redirect(reverse('admin:index')) #reverse retorna a url de index:admin   
            return redirect('indexComunidade')
    
    
class CadastrarView(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('indexComunidade')
        return render(request, 'cadastro.html')
        return redirect('questionario')

    def post(self,request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        foto = request.FILES.get('imagem')
        
        print(foto)
        if(' ' in senha):
            messages.add_message(request, constants.WARNING, "Não é possível cadastrar uma senha com espaços em branco")
            return render(request, 'cadastro.html')
        if(len(senha) < 4):
            messages.add_message(request, constants.WARNING, "Senha muito curta")
            return render(request, 'cadastro.html')
        usuarioExist = Usuario.objects.filter(username=username)
        if(usuarioExist):
            messages.add_message(request, constants.ERROR, "Já há um usuário com esse nome")
            return render(request, 'cadastro.html')
        emailExist = Usuario.objects.filter(email=email)
        if(emailExist):
            messages.add_message(request, constants.ERROR, "Esse e-mail já esta registrado")
            return render(request, 'cadastro.html')
        try:
            user = Usuario.objects.create_user(
                username=username,
                email=email,
                password=senha,
               
            )
            if foto:
                user.foto =foto
                
            user.save() 
                        
            messages.add_message(request, constants.SUCCESS, "Usuario criado com sucesso, seja  bem-vindo")
            auth.login(request, user)
            return redirect('questionario')
        except Exception as e:
            
            messages.add_message(request, constants.DEBUG, f'Erro interno do sitema {e}')
            return render(request, 'cadastro.html')

class ForgetView(View):
    template_name= 'recuperacao.html'
    def get(self,request, *args, **kwargs):
        return render(request, self.template_name, {'carregar':'email_insert'})
    def post(self,request, *args, **kwargs):
        acao = request.GET.get('acao')

        if acao == 'insert_code':
            email = request.POST.get('email').strip()
            usuario =Usuario.objects.filter(email=email)
            if usuario:
                
                token = ' '.join(str(secrets.randbelow(10)) for _ in range(6))
                enviar_email_async(email_destinatario=email, codigo_aleatorio=token)
                if token.split('+')[0] == 'error':

                    messages.add_message(request, constants.ERROR, f"Erro do servidor {token.split('+')[1]}")
                    return render(request, self.template_name)
                
                request.session['emailNovaSenha'] = email
                request.session['token'] = token #salvar isso em outra coisa, que se abrir o inspecionar
             
                return render(request,'recuperacao.html',{'token': token, 'carregar':'insert_code', 'user':usuario[0]})
            
            else:
                messages.add_message(request, constants.ERROR, 'Email não correspondente a nenhuma conta')
                return render(request, 'recuperacao.html', {'carregar':'email_insert', 'user':usuario}) 
        
        elif acao =='new_password':
            codigo = request.POST.get('codigo')
            token = (request.session.get('token')).replace(' ', '')
            print(f'Valor token {token}')
            if  codigo ==token:
               usuario_email =request.session.get('emailNovaSenha')
               usuario = Usuario.objects.get(email=usuario_email)
               return render(request, 'recuperacao.html', {'carregar':'new_password', 'user':usuario}) # nem precisava de valor já que ta no else mas melhor colcoar
            else:
                messages.add_message(request, constants.ERROR, 'O código esta incorreto, por favor verfique')
                return render(request, 'recuperacao.html', {'carregar':'insert_code'} )
class RedefinirSenha(View):
    def get(self, request, *args, **kawrgs):
        return HttpResponse('Deu get no redefinir senha')
    def post(self, request, *args, **kwargs):
        email = request.session.get('emailNovaSenha')
        user = Usuario.objects.get(email=email)
        senha = request.POST.get('senha')
        user.set_password(senha)
        user.save()
        for _ in range(0,100000000): # só para enrolar um pouco, tava muito rápido a recarga
            pass
        user.save()
        messages.add_message(request, constants.SUCCESS, "Senha redefinida com sucesso")

        return  redirect('login')

class Questionario(View):
    template_name = "questionario.html"
    login_url = 'login'
    def get(self, request, *args, **kawrgs):
        perguntas =PerguntaDoQuestionario.objects.all()
     
        opcoes = Opcao.objects.all()
         
        
        return render(request, 'questionario.html', {'perguntas': perguntas, 'opcoes': opcoes})
    def post(self, request, *args, **kwargs):    
        dados = request.POST.copy() #deixa mutável
        dados = dict(dados)
        
        dados_sem_csrf = {}
        cont = 0
        for i, j in dados.items():
            if cont == 0:
                cont+=1
                continue
           
            dados_sem_csrf[i] = j
        dados = dados_sem_csrf
       
            

        user = request.user
        
        for key, value in dados.items():
            value = value[0].strip()
            
            if PerguntaDoQuestionario.objects.filter(tipo_input=Input.objects.get(nome='checkbox'), titulo_pergunta=key) :
              
                dados_check = dados[key]
             
                for dado in dados_check:
                    dado_selecionado = Opcao.objects.get(nome=dado)
                    m = PergutasCheckBox(
                        opcao = dado_selecionado,
                        usuario=user
                    )
                    m.save()

                
            else:
                 
                 p = PerguntaUsuario(
                     user=user,
                     pergunta= PerguntaDoQuestionario.objects.get(titulo_pergunta=key),
                     resposta=value
                 )
                 p.save()

        return redirect('indexComunidade')
            
# InMemoryLoadedFile  -Armazena no Ram quando é menos de 2mb django usa ele
# Temporary LoadedFile - >2.5 memoria usa isso
# 
# 
# 
