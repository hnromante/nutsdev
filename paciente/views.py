from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from recomendacion.models import Recomendacion
from django.shortcuts import get_object_or_404
from paciente.models import Paciente
from django.http import Http404
from django.http import JsonResponse
from paciente.models import FichaNutricional
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
    paciente = request.user.paciente
    recomendacion = Recomendacion.objects.get(paciente=paciente)
    
    return render(request, 'paciente/index.html', {'observacion': recomendacion.observacion})

def evaluacion_nutricional(request):
    paciente = request.user.paciente
    ficha_nutricional = FichaNutricional.objects.get(paciente=paciente)
    return render(request, 'paciente/evaluacion_nutricional.html', {'ficha_nutricional': ficha_nutricional})

def mi_nutricionista(request):
    paciente = request.user.paciente
    nutricionista = paciente.nutricionista
    return render(request, 'paciente/mi_nutricionista.html', {'nutricionista': nutricionista})


def minuta_paciente(request, pk_paciente):
    if Paciente.objects.filter(pk=pk_paciente).exists():
        paciente = Paciente.objects.get(pk=pk_paciente)
        recomendacion = Recomendacion.objects.get(paciente=paciente)
        return JsonResponse(recomendacion.comidas, safe=False)
    else: 
        raise Http404

def grupos_permitidos(request, pk_paciente):
    if Paciente.objects.filter(pk=pk_paciente).exists():
        paciente = Paciente.objects.get(pk=pk_paciente)
        recomendacion = Recomendacion.objects.get(paciente=paciente)
        return JsonResponse(recomendacion.grupos_permitidos, safe=False)
    else: 
        raise Http404
