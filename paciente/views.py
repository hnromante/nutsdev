from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
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
    return render(request, 'paciente/index.html')