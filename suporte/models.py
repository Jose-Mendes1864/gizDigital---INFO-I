from django.db import models
from autenticacao.models import Usuario
from enum import Enum
# Create your models here.
class StatusEnum(Enum):
    RESOLVIDO = 'Resolvido'
    EM_ANDAMENTO = 'Em andamento'
    NAO_ANALISADO = 'Não analisado'

class MotivoSuporte(models.Model):
    motivo = models.CharField(max_length=60)
    class Meta:
        verbose_name_plural = 'Motivos de solicitação do suporte'
    def __str__(self):
        return self.motivo
    
    
class RequisicaoSuporte(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    motivo = models.ForeignKey(MotivoSuporte, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices= [(tag.name, tag.value) for tag in StatusEnum], default=StatusEnum.NAO_ANALISADO.name)
    descricao = models.TextField()
    foto = models.FileField(upload_to='usuario/requisicao', null=True, blank=True)
    class Meta:
        ordering = ['status']
        
    def __str__(self):
        return f'{self.motivo} - {self.status}'