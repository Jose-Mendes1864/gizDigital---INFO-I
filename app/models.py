from django.db import models
from autenticacao.models import Usuario
from enum import Enum
from .functionsModels import get_usuario_padrao
# Create your models here.



class Etiqueta(models.Model):
    corRGB = models.CharField(max_length=13)
    nome = models.CharField(max_length=200)
    def __str__(self):
        return self.nome
class Comunidade(models.Model):
    nome = models.CharField(max_length=60 )
    descricao = models.TextField(verbose_name='descrições')
    etiquetas = models.ManyToManyField(Etiqueta,related_name='comunidades')
    membros = models.ManyToManyField(Usuario, related_name='comunidades', null=True, blank=True)
    
    capa_comunidade = models.FileField(upload_to='comunidade/capa')


    def __str__(self):
        return f'Comunidade - {self.nome}'


class Post(models.Model):
    comunidade = models.ForeignKey(Comunidade,on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    conteudo = models.CharField(max_length=400)
    foto = models.ImageField(upload_to=f'usuario/posts', null=True, blank=True)
    #preciso aqui identific ra imagme de quem é no banco de dados ex.: post1jose.png
    
    data_criacao = models.DateTimeField()
    def __str__(self):
        return f'{self.usuario.username} conteudo: {self.conteudo[:20 ] + '...'}'

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_DEFAULT, default=get_usuario_padrao)
    criacao = models.DateTimeField()
    conteudo = models.TextField()
    def __str__(self):
        return f'{self.usuario.username} - {self.conteudo}'

class Arquivo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comunidade = models.ForeignKey(Comunidade, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='comunidade/arquivos')
    ext = models.CharField(max_length=10,blank=True, null=True )
    def __str__(self):
        return f'{self.usuario.username} - {self.titulo}'
    
class Reuniao(models.Model):
    criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comunidade =models.ForeignKey(Comunidade, on_delete=models.CASCADE)
    tematica = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100, default=None)
    url_da_reuniao = models.CharField(max_length=100)
    data_hora = models.DateTimeField()
    class Meta:
        verbose_name_plural = 'Reuniões'
    def __str__(self):
        return f'{self.criador} -  {self.tematica} - {self.data_hora.strftime("%d de %B de %Y, %Hh%M")}'
    
