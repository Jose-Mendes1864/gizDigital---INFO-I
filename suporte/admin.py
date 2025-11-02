from django.contrib import admin
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django_object_actions import DjangoObjectActions
import urllib.parse
# Register your models here.
admin.site.register(MotivoSuporte)
@admin.register(RequisicaoSuporte)
class RequisaoSuporteAdmin(DjangoObjectActions,admin.ModelAdmin):
    search_fields = ['solicitante', 'motivo']
    change_actions = ('enviar_email',)

    def enviar_email(self, request, obj):
        email = obj.solicitante.email
        subject = urllib.parse.quote(f"Equipe de suporte Giz Digital") #urllib.parse.quote usado para codificar o assunto (subject) e corpo (body) do email, evitando problemas com espaços ou caracteres especiais.
        body = urllib.parse.quote(f"Olá, vi que você solicitou suporte")
        gmail_link = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={subject}&body={body}"
        html = f'''
        <html>
            <head>
                <script>
                    window.open("{gmail_link}", "_blank");  // abre Gmail em nova aba
                    window.location = "{request.META.get('HTTP_REFERER', '/admin/')}"; // volta para o admin
                </script>
            </head>
            <body></body>
        </html>
        '''
        return HttpResponse(html)
            #HttpResponse → para retornar HTML/JS no admin.
    enviar_email.label = "Enviar Email"


