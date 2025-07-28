from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import  Usuario
from django.contrib import messages
from django.contrib.messages import constants
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
            messages.add_message(request, constants.WARNING, "Já há um usuário com esse nome")
            return render(request, 'cadastro.html')
        emailExist = Usuario.objects.filter(email=email)
        if(emailExist):
            messages.add_message(request, constants.WARNING, "Esse e-mail já esta registrado")
            return render(request, 'cadastro.html')
        try:

            user = Usuario(
                username=username,
                email=email,
                password=senha
            )
            user.save()
            messages.add_message(request, constants.SUCCESS, "Usuario criado com sucesso, seja  bem-vindo")

            return render(request, 'login.html')
        except:
            
            messages.DEBUG(request, constants.WARNING, "Erro interno do sitema")
            return render(request, 'cadastro.html')

               

