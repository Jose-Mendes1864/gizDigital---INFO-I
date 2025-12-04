from django.contrib import admin
from .models import Usuario, Input,Opcao, PerguntaDoQuestionario,PerguntaUsuario, PergutasCheckBox
from .functions import capitalizadoToSnakeCase
# pagina de administração:
from app.models import Reuniao, Comentario,Post
from app.admin import PostInline, ComentarioInline,ArquivoInline
from django.contrib.auth.models import Group

# versão original:

admin.site.register(PerguntaUsuario)
admin.site.unregister(Group)
admin.site.register(PergutasCheckBox)



class PerguntaInline(admin.TabularInline):
    list_display = ['pergunta', 'resposta']
    model = PerguntaUsuario
    extra = 0

class PerguntaCheckBoxInline(admin.TabularInline):
    list_display = ['opcao']
    model = PergutasCheckBox
    extra = 0

@admin.register(Opcao)
@admin.register(PerguntaDoQuestionario)
class PerguntaDoQuestionarioAdmin(admin.ModelAdmin):
  
    def save_model(self, request, obj, form, change):
        if not change:  # só na criação
            obj.titulo_pergunta = capitalizadoToSnakeCase(obj.titulo_pergunta)
        super().save_model(request, obj, form, change)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    inlines = [PerguntaInline, PerguntaCheckBoxInline, ArquivoInline, PostInline,  ComentarioInline,]
    list_display = ('username', 'email')
    readonly_fields = ('date_joined',)
    search_fields = ['username', 'email']
    fieldsets = (
    ('Informações', {'fields': ('username', 'foto', 'email', 'pontuacao', 'date_joined')}),
    ('Permissões', {'fields': ('is_staff', 'is_superuser','is_active')}),
)