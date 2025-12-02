from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from  .models import MotivoSuporte, RequisicaoSuporte
from django.contrib import messages 
from django.contrib.messages import constants
# Create your views here.
class SuporteView(View):
    def get(self,request, *args,**kwargs):
        motivos = MotivoSuporte.objects.all()
        return render(request, 'suporte.html', {'motivos':motivos})

    def post(self, request, *args,**kwargs):
        motivo = request.POST.get('motivo')
        mensagem =  request.POST.get('mensagem')
        imagem = request.POST.get('imagem')
        solicitacao = RequisicaoSuporte(
            solicitante=request.user,
            motivo= MotivoSuporte.objects.get(motivo=motivo),
            foto = imagem,
            descricao=mensagem,
        )
        print(f'Imagem: {imagem}, mensagem {mensagem}, motivo {motivo}')
        solicitacao.save()
        messages.add_message(request, constants.SUCCESS, 'Sua solicitação de suporte foi um sucesso, logo receberá um retorno pelo seu e-mail')
        
        return render(request, 'suporte.html')

