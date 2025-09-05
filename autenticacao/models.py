from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import *
from .functions import  caminho_imagem
# Create your models here.

class Usuario(AbstractUser):
    tipo_perfil = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in TipoPerfilEnum], default=TipoPerfilEnum.PADRAO.name)
    # is_active supre o statusPerfil
    # usrname o django auth já temmpo
   
    nome_completo = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    # seha o django já tem
   
    biografia =models.TextField(null=True, blank=True)
    pasta_destino = models.CharField(max_length=100, default='usuario/foto', editable=False)
    foto = models.FileField(upload_to=caminho_imagem, default='usuario/foto/defaultFotoPerfil.jpg')
    pontuacao =models.FloatField(default=3, null=True, blank=True)
    #  data criação já possui

    USERNAME_FIELD = 'email'  # define email comocampo para o auth.authenticate, memso asism é nessecssário username=email
    REQUIRED_FIELDS = ['username'] # são campo obrigatório ao criar o superusuario deixamos em branco porque um deles é o email mas já ta unique e é o username_field ali ent não precisa

class Input(models.Model):
    nome  = models.CharField(max_length=30)
    def __str__(self):
        return self.nome

class PerguntaDoQuestionario(models.Model):
    titulo_pergunta = models.CharField(max_length=40)
    texto_pergunta =  models.CharField(max_length=700)
    tipo_input = models.ForeignKey(Input, on_delete=models.DO_NOTHING)
    placeholder  = models.CharField(max_length=50, default=" ", blank=True, null=True)
    
    def __str__(self):
        return  self.titulo_pergunta
class Opcao(models.Model):
    nome = models.CharField(max_length=60)
    pergunta = models.ForeignKey(PerguntaDoQuestionario, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.nome

class PerguntaUsuario(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(PerguntaDoQuestionario, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=500)
    def __str__(self):
        return f'{self.user} - {self.pergunta.titulo_pergunta}'
    
class MaterialUsuarios(models.Model):
    opcao = models.ForeignKey(Opcao, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
