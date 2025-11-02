from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import *
from django.core.files.base import ContentFile

from .functions import  caminho_imagem, tiraSnakeCase,capitalizadoToSnakeCase

# Create your models here.

class Usuario(AbstractUser):
    tipo_perfil = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in TipoPerfilEnum], default=TipoPerfilEnum.PADRAO.name)
    # is_active supre o statusPerfil
    # usrname o django auth já temmpo
   
    email = models.EmailField(unique=True)
    # seha o django já tem
   
   
    pasta_destino = models.CharField(max_length=100, default='usuario/foto', editable=False)
    foto = models.FileField(upload_to=caminho_imagem, default='usuario/foto/defaultFotoPerfil.jpg')
    pontuacao =models.FloatField(default=2, null=True, blank=True)
    #  data criação já possui

    USERNAME_FIELD = 'email'  # define email comocampo para o auth.authenticate, memso asism é nessecssário username=email
    REQUIRED_FIELDS = ['username'] # são campo obrigatório ao criar o superusuario deixamos em branco porque um deles é o email mas já ta unique e é o username_field ali ent não precisa
    class Meta:
        ordering = ['email']
    
    def __str__(self):
        return f'{self.username} - {self.email}'
    def save(self, *args, **kwargs):
        try:
            # pegar objeto antigo do banco
            antigo = Usuario.objects.get(pk=self.pk)
            if antigo.foto and antigo.foto != self.foto and antigo.foto.name != 'usuario/foto/defaultFotoPerfil.jpg':
                antigo.foto.delete(save=False)  # deleta o arquivo antigo
        except Usuario.DoesNotExist:
            pass
        super().save(*args, **kwargs)

class Input(models.Model):
    nome  = models.CharField(max_length=30)
    def __str__(self):
        return self.nome

class PerguntaDoQuestionario(models.Model):
    titulo_pergunta = models.CharField(max_length=40)
    texto_pergunta =  models.CharField(max_length=700)
    tipo_input = models.ForeignKey(Input, on_delete=models.DO_NOTHING)
    placeholder  = models.CharField(max_length=50, default=" ", blank=True, null=True)
    aparecer_no_perfil = models.BooleanField(default=True)

    def __str__(self):
        return  tiraSnakeCase(str(self.titulo_pergunta))
class Opcao(models.Model):
    nome = models.CharField(max_length=60)
    pergunta = models.ForeignKey(PerguntaDoQuestionario, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Opções dos inputs'
        ordering = ['pergunta',]
    def __str__(self):
        return f'{tiraSnakeCase(str(self.pergunta))}: opção - {self.nome}'

class PerguntaUsuario(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(PerguntaDoQuestionario, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=500)
    class Meta:
        verbose_name_plural = 'Respostas únicas do questionario'
        ordering = ['user']
    def __str__(self):
        return f'{self.user} - {self.pergunta.titulo_pergunta} - {self.resposta}'
    
class PergutasCheckBox(models.Model):
    opcao = models.ForeignKey(Opcao, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    class Meta:
        ordering = ['usuario']
        verbose_name_plural = 'respostas com mais de uma opção'     
    def __str__(self) -> str:
        return f'{self.usuario.username} - {self.opcao} '
    
