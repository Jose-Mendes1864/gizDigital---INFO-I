from autenticacao.models import Usuario
from django.shortcuts import HttpResponse
from .models import Arquivo,Reuniao
from autenticacao.models import *
from .models import  *
import re
from django.utils import timezone



def tiraSnakeCase(texto):
    corrigido =  texto.replace('_', ' ')
    
   
    
    return corrigido.capitalize()



def capitalizadoToSnakeCase(name):
    name = name.replace(' ', '_')
    return name.lower()
def pega_dados_comunidade(carrega, id_comunidade):
    dados = ''
    if carrega == 'posts':
        pass
    elif carrega == 'eventos':
        dados = Reuniao.objects.filter(comunidade_id=int(id_comunidade))
    elif carrega == 'materiais':
        dados = Arquivo.objects.filter(comunidade__id = int(id_comunidade))

    return dados

def get_dados_input(input):
    perguntas_questionario = PerguntaDoQuestionario.objects.filter(tipo_input__nome=input)
    dicionario = {}
    for i in perguntas_questionario:
        dicionario[tiraSnakeCase(i.titulo_pergunta)] = Opcao.objects.filter(pergunta__titulo_pergunta=i.titulo_pergunta)
    return dicionario
def adiciona_objetos_com_checkbox(request,perguntas_com_checkbox, dados_usuario):
    # debug = {}
    for  p in perguntas_com_checkbox:
        # print(f'Valor de p e {p}')
        dados_usuario[tiraSnakeCase(str(p.titulo_pergunta)) ] = PergutasCheckBox.objects.filter(usuario=request.user).filter(opcao__pergunta=p)
        # debug[tiraSnakeCase(str(p.titulo_pergunta))] = PergutasCheckBox.objects.filter(usuario=request.user).filter(opcao__pergunta=p)

    # for key, value in debug.items():
    #     print(f'KEY {key} value - {value}')
    # print(dados_usuario)
    return dados_usuario
def estrela(request):
    # auqi é chamado quando o usuário adiciona um post
    user = request.user
    dias_desde_criacao = (timezone.now() - user.date_joined).days 
            # só é atualizadoquando ele adiciona um post
    media_ponderada = (3 * (dias_desde_criacao/60) + Post.objects.filter(usuario = user).count())/4
    if media_ponderada < 2:
        media_ponderada = 2
    
    media_ponderada = round(media_ponderada)
    if media_ponderada >5:
        media_ponderada = 5
    user.pontuacao = media_ponderada
    user.save()

 # media_ponderada  = 3* (dias_criou_conta/60) + 2*quant_posts / 3+2

