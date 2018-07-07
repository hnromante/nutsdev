from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from recomendacion.models import Recomendacion
from django.shortcuts import get_object_or_404
from paciente.models import Paciente
from django.http import Http404
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='/login-paciente/')
def inicio_paci(request):
    """
    Controlador de dashboard del paciente. Muestra información útil al paciente.
    :param request:
    :return:
    """
    if not request.user.es_paciente:
        messages.error(request, 'Usted no esta registrado como paciente')
        return HttpResponseRedirect('/login-paciente')
    # paciente = get_object_or_404(Paciente, pk=request.user.paciente.pk
    
    
    return render(request, 'paciente/index.html')

def minuta_paciente(request, pk_paciente):
    if Paciente.objects.filter(pk=pk_paciente).exists():
        paciente = Paciente.objects.get(pk=pk_paciente)
        recomendacion = Recomendacion.objects.get(paciente=paciente)
        return JsonResponse(recomendacion.comidas, safe=False)
    else: 
        raise Http404