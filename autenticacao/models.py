from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import *
from .functions import  *
# Create your models here.

class Usuario(AbstractUser):
    tipo_perfil = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in TipoPerfilEnum], default=TipoPerfilEnum.PADRAO.name)
    # is_active supre o statusPerfil
    # usrname o django auth já tem
    nome_completo = models.CharField(max_length=100, null=True, blank=True)
    # email o django já tem
    # seha o django já tem
    
    biografia =models.TextField(null=True, blank=True)
    pasta_destino = models.CharField(max_length=100, default='usuario/foto', editable=False)
    foto = models.FileField(upload_to=caminho_imagem, null=True, blank=True)
    pontuacao =models.FloatField(default=3, null=True, blank=True)
    #  data criação já possui