from autenticacao.models import Usuario
def get_usuario_padrao():
    from autenticacao.models import Usuario
    usuario, _ = Usuario.objects.get_or_create(username="usuario_padrao", defaults={
        "email": "usuario@padrao.com",
        "password": "123456"
    })
    return usuario.id