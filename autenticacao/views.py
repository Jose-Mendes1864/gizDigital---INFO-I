from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

from .models import  Usuario
from .functions import enviar_email
import secrets

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
        if request.user.is_authenticated:
            return HttpResponse("Usuario já esta autenticado " + request.user.username + ' Retornar para pagina index')
 
        email = request.POST.get('email').strip()
        senha = request.POST.get('senha')
        print(email)
        print(senha)

        usuario = auth.authenticate(request, username=email, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Por favor insira email e senha corretos')
            return redirect('login')
        else:
            auth.login(request, usuario)

            return HttpResponse("Usuario já esta autenticado " + request.user.username + ' Retornar para pagina index')
    
    
class CadastrarView(View):
    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("Usuario já esta autenticado" + request.user.username)
        return render(request, 'cadastro.html')
    def post(self,request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
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
                password=senha
            )
            user.save()
            messages.add_message(request, constants.SUCCESS, "Usuario criado com sucesso, seja  bem-vindo")
            auth.login(request, user)
            return render(request, 'questionario.html')
        except:
            
            messages.DEBUG(request, constants.WARNING, "Erro interno do sitema")
            return render(request, 'cadastro.html')

class ForgetView(View):
    def get(self,request, *args, **kwargs):
        return render(request, 'recuperacao.html')
    def post(self,request, *args, **kwargs):
        email = request.POST.get('email').strip()
        if Usuario.objects.filter(email=email):
            token  = enviar_email(email_destinatario=email)
            if token.split('+')[0] == 'error':
                messages.add_message(request, constants.ERROR, f'Erro do servidor {token.split('+')[1]}')
                return render(request, 'recuperacao.html')
            return HttpResponse(f'Token enviado, ele é = {token}')
        else:
            messages.add_message(request, constants.ERROR, 'Email não encontrado')

        return render(request, 'recuperacao.html')

        return HttpResponse('post')
    
class ComunidadesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'comuGeral.html')

class ComunidadeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'comuBase.html')
    
class PerfilEdit(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'perfilEdit.html') 
        # Fala josé, outro recado aqui! Esse perfil edit provavelmente nem classe é! já que é apenas um atributo da pagina de perfil maaas... Não temos como vai ser o perfil, só a edição -> conversar com a sarah sobre isso
