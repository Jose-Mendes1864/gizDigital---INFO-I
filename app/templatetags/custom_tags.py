from django import template
from app.functions import capitalizadoToSnakeCase
from autenticacao.models import *
from app.models import Post
register = template.Library()

@register.filter
def dict_get(d, key):
   
    try:
        lista_nomes = []
        if PerguntaDoQuestionario.objects.filter(titulo_pergunta=capitalizadoToSnakeCase(key),tipo_input__nome='checkbox' ):
            lista_objetos = list(d.get(key))
            
            
           
            for i in lista_objetos:
                
                lista_nomes.append(i.opcao.nome)
           
        else: # se é um select
           
                lista_nomes.append(d.get(key, []))
            
        

        return ', '.join(map(str, lista_nomes))
    except Exception as e:
         print(f'O erro é {e}')
         return 'Não retonrou nada'


@register.filter
def quebra_linha(texto, tamanho=80):
    resultado = ""
    for i in range(0, len(texto), tamanho):
        resultado += texto[i:i+tamanho] + "<br>"
    return resultado

@register.filter
def filtrar_comentarios(post_id):
    resultado = Post.objects.filter(id=post_id)
    print(f'Resultado: {resultado}')
    return resultado