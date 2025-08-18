from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.
class ComunidadesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'comuGeral.html')
      

class ComunidadeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'comuBase.html')
    
class PerfilEdit(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'perfilEdit.html') 