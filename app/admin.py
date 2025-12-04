from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Etiqueta)
admin.site.register(Arquivo)

admin.site.register(Comentario)

class ArquivoInline(admin.StackedInline):
    list_display = ('comunidade', 'titulo','arquivo')
    model = Arquivo
    extra = 0
    class Media:
        css = {'all': ('css/custom.css',)}
class PostInline(admin.StackedInline):
    list_display = ('comunidade', 'conteudo' 'foto','data_criacao')
    model = Post
    extra = 0
    class Media:
        css = {'all': ('css/custom.css',)}


class ComentarioInline(admin.StackedInline):
    list_display = ('usuario', 'conteudo',)
    model = Comentario
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': admin.widgets.AdminTextareaWidget(attrs={
            'rows':3,
            'cols': 30,
            'style': 'max-width:420px; white-space:normal; word-wrap:break-word;'
        })},
    }

@admin.register(Comunidade)
class ComunidadeAdmin(admin.ModelAdmin):
   inlines = [PostInline]
 
   autocomplete_fields = ['membros']
   search_fields = ['nome', 'etiquetas__nome']
   search_help_text = "Busque pelo nome ou etiquetas"

 
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ComentarioInline]
    list_display =  ['usuario','conteudo','comunidade', 'data_criacao']
    search_fields = ['usuario__username', 'comunidade__nome']
    search_help_text = "Busque pelo criador do post ou comunidade"
    ordering = ['-data_criacao']


@admin.register(Reuniao)
class ReuniaoAdmin(admin.ModelAdmin):
   
    list_display =  ['tematica', 'data_hora']
    ordering = ['-data_hora']
    search_fields = ['tematica', 'criador__username']
    search_help_text = "Busque pelo criador ou temática"


