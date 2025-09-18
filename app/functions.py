from autenticacao.models import Usuario
from django.shortcuts import HttpResponse
def get_usuario_padrao():
    from autenticacao.models import Usuario
    usuario, _ = Usuario.objects.get_or_create(username="usuario_padrao", defaults={
        "email": "usuario@padrao.com",
        "password": "123456"
    })
    return usuario.id

def tiraCamelCase(texto):
    corrigido = ''
    for i in texto:
        if i.isupper():
            corrigido+= ' ' + i.lower()
        else:
            corrigido+=i
    return corrigido.capitalize()

