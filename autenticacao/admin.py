from django.contrib import admin
from .models import Usuario, Input,Opcao, PerguntaDoQuestionario,PerguntaUsuario, MaterialUsuarios

admin.site.register(Usuario)
admin.site.register(Input)
admin.site.register(PerguntaDoQuestionario)
admin.site.register(Opcao)
admin.site.register(PerguntaUsuario)
admin.site.register(MaterialUsuarios)


