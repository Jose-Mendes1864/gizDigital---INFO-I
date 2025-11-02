from autenticacao.models import Usuario
from django.shortcuts import HttpResponse
from .models import Arquivo,Reuniao
from autenticacao.models import *
from .models import  *
import re
from django.utils import timezone
from django.db.models import Count


def tiraSnakeCase(texto):
    corrigido =  texto.replace('_', ' ')
    
    
    return corrigido.capitalize()



def capitalizadoToSnakeCase(name):
    name = name.replace(' ', '_')
    return name.lower()
def pega_dados_comunidade(carrega, id_comunidade):
    dados = ''
    if carrega == 'posts':
        dados = Post.objects.filter(comunidade__id=id_comunidade).order_by('-data_criacao')  # ordena por ordem inversa de id
    elif carrega == 'eventos':
        dados = Reuniao.objects.filter(comunidade_id=int(id_comunidade)).order_by('-data_hora')  # ordena por ordem inversa de id
    elif carrega == 'materiais':
        dados = Arquivo.objects.filter(comunidade__id = int(id_comunidade)).order_by('-id')  # ordena por ordem inversa de id
   
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


# Comunidad eindex
def verifica_se(entrada, areas_user, leciona_para):
    areas_user_nome = [i.opcao.nome for i in areas_user]
    leciona_para_nome = [i.opcao.nome for i in leciona_para]  

    if entrada == 'area_do_saber':
        retorno = Comunidade.objects.filter(
            etiquetas__nome__in=areas_user_nome
        ).distinct().exclude(etiquetas__nome__in=leciona_para_nome)
    elif entrada == 'leciona':
        retorno = Comunidade.objects.filter(
            etiquetas__nome__in=leciona_para_nome    
        ).distinct().exclude(etiquetas__nome__in=areas_user_nome)
    elif entrada == 'area_saber + leciona':

        retorno =Comunidade.objects.filter(
                    etiquetas__nome__in=areas_user_nome).filter(etiquetas__nome__in=leciona_para_nome               
                ).distinct().annotate(
                    num_membros=Count('membros')
                ).order_by('-num_membros') 
                        #annotate(num_membros=Count('membros')) → cria um campo temporário num_membros com a contagem de membros.
                        #order_by('-num_membros') → ordena as comunidades do maior para o menor número de membros.
                        # esse in verifica se tem um valor dentrod e uma list esse anotate anota a a
                    
    return retorno
