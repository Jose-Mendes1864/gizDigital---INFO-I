from autenticacao.models import Usuario
from django.shortcuts import HttpResponse
from .models import Arquivo,Reuniao
from autenticacao.models import *
import re

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
