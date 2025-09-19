from autenticacao.models import Usuario
from django.shortcuts import HttpResponse
from .models import Arquivo


def tiraCamelCase(texto):
    corrigido = ''
    for i in texto:
        if i.isupper():
            corrigido+= ' ' + i.lower()
        else:
            corrigido+=i
    return corrigido.capitalize()

def pega_dados_comunidade(carrega, id_comunidade):
    dados = ''
    if carrega == 'posts':
        pass
    elif carrega == 'eventos':
        pass
    elif carrega == 'materiais':
        dados = Arquivo.objects.filter(comunidade__id = int(id_comunidade))

    return dados