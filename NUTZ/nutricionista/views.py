from django.shortcuts import render
from nutricionista.models import Nutricionista
from django.views.generic.list import ListView
from paciente.models import Paciente
from django.apps import apps
from .forms import (
    FormAddPaciente,
)
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Create your views here.
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from cuentas.models import User




def calculadora(request):
    return render(request,template_name='nutricionista/calculadora.html')

@login_required(login_url='/login-nutricionista/')
def inicio_nutri(request):
    if not request.user.es_nutri:
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')

    return render(request,'nutricionista/index.html')


@login_required(login_url='/login-nutricionista/')
def mis_pacientes(request):
    if not request.user.es_nutri:
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
        
    menssages = messages.get_messages(request)
    if request.method == "POST":
        form_add_paciente = FormAddPaciente(request.POST)
        if form_add_paciente.is_valid():
            nutricionista = request.user.nutricionista
            user_paciente = User.objects.create_user(rut=form_add_paciente.cleaned_data['rut'], 
                                                email= form_add_paciente.cleaned_data['email'], 
                                                password='password123', 
                                                es_paciente=True,
                                                es_nutri=False)
            paciente = Paciente.objects.create( user=user_paciente, 
                                                nutricionista=nutricionista,
                                                ocupacion=form_add_paciente.cleaned_data['ocupacion'],
                                                nacionalidad=form_add_paciente.cleaned_data['nacionalidad'],
                                                observacion=form_add_paciente.cleaned_data['observacion'],
                                                peso=form_add_paciente.cleaned_data['peso'],
                                                glicemia_mgdl=form_add_paciente.cleaned_data['glicemia_mgdl'],
                                                )
            messages.success(request, 'Paciente creado correctamente.')

    else:
        form_add_paciente = FormAddPaciente()
    context = dict()
    context['form'] = form_add_paciente
    context['menssages'] = menssages
    pacientes = Paciente.objects.filter(nutricionista=request.user.nutricionista)
    context['pacientes'] = pacientes
    return render(request, template_name='nutricionista/mis_pacientes.html', context=context)


