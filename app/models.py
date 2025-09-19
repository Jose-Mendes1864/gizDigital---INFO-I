from django.db import models
from autenticacao.models import Usuario
from enum import Enum
from .functionsModels import get_usuario_padrao
# Create your models here.

class StatusEnum(Enum):
    RESOLVIDO = 'Resolvido'
    EM_ANDAMENTO = 'Em andamento'
    NAO_ANALISADO = 'Não analisado'
    
class Etiqueta(models.Model):
    corRGB = models.CharField(max_length=13)
    nome = models.CharField(max_length=200)
    def __str__(self):
        return self.nome
class Comunidade(models.Model):
    nome = models.CharField(max_length=60 )
    descricao = models.TextField(verbose_name='descrições')
    etiquetas = models.ManyToManyField(Etiqueta,related_name='comunidades')
    membros = models.ManyToManyField(Usuario, related_name='comunidades')
  
    capa_comunidade = models.FileField(upload_to='comunidade/capa')


    def __str__(self):
        return f'Comunidade - {self.nome}'


class Post(models.Model):
    comunidade = models.ForeignKey(Comunidade,on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descricao_post = models.CharField(max_length=400)
    foto = models.ImageField(upload_to=f'usuario/posts', null=True, blank=True)
    #preciso aqui identific ra imagme de quem é no banco de dados ex.: post1jose.png
    curtidas = models.IntegerField(default=0)
    data_criacao = models.DateTimeField()
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_DEFAULT, default=get_usuario_padrao)
    criacao = models.DateTimeField()
    conteudo = models.TextField()
class MotivoSuporte(models.Model):
    motivo = models.CharField(max_length=60)
    def __str__(self):
        return self.motivo
    
class RequisicaoSuporte(models.Model):
    motivo = models.ForeignKey(MotivoSuporte, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices= [(tag.name, tag.value) for tag in StatusEnum])
    descricao = models.TextField()
    foto = models.FileField(upload_to='usuario/requisicao', null=True, blank=True)
class Arquivo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comunidade = models.ForeignKey(Comunidade, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='comunidade/arquivos')
    ext = models.CharField(max_length=10,blank=True, null=True )