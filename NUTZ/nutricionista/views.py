from django.shortcuts import render
from nutricionista.models import Nutricionista, Menu, PautaAlimentaria
from django.views.generic.list import ListView
from paciente.models import Paciente
from django.apps import apps
from .forms import (
    FormAddPaciente,
    FormPerfil,
    FormMenu,
    FormPautaAlimentaria
)
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
# Create your views here.
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core import serializers
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
        messages.warning(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    context = dict()
    pacientes = Paciente.objects.filter(nutricionista=request.user.nutricionista)
    context['pacientes'] = pacientes
    return render(request, template_name='nutricionista/pacientes.html', context=context)


@login_required(login_url='/login-nutricionista/')
def agregar_paciente(request):
    if not request.user.es_nutri:
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    if request.method == "POST":
        form = FormAddPaciente(request.POST)
        if form.is_valid():
            nutricionista = request.user.nutricionista
            user = User.objects.create_user(rut=form.cleaned_data['rut'], 
                                                email= form.cleaned_data['email'], 
                                                password='password123', 
                                                es_paciente=True,
                                                es_nutri=False)
            Paciente.objects.create(user=user, nutricionista=nutricionista,
                                    ocupacion=form.cleaned_data['ocupacion'],
                                    nacionalidad=form.cleaned_data['nacionalidad'],
                                    observacion=form.cleaned_data['observacion'],
                                    peso=form.cleaned_data['peso'],
                                    glicemia_mgdl=form.cleaned_data['glicemia_mgdl'])
            messages.success(request, 'Paciente creado correctamente.')
    else:
        form = FormAddPaciente()
    return render(request, template_name='nutricionista/pacientes_agregar.html', context={'form':form})


@login_required(login_url='/login-nutricionista/')
def mi_perfil(request):
    if not request.user.es_nutri:
        messages.error(request,'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    if request.method == "POST":
        form = FormPerfil(request.POST)
        if form.is_valid():
            pass
    else:
        form = FormPerfil(instance=request.user)
    return render(request, 'nutricionista/perfil.html', {'form':form})


@login_required(login_url='/login-nutricionista/')
def mis_menus(request):
    if not request.user.es_nutri:
        messages.error(request,'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    if request.method == "POST":
        form = FormMenu(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.nutricionista = request.user.nutricionista
            form.save()
    else:
        form = FormMenu()
    menus = Menu.objects.filter(nutricionista=request.user.nutricionista)
    print("****menus****")
    print(menus)
    print(len(menus))
    return render(request, 'nutricionista/mis_menus.html',{'form':form,
                                                            'menus':menus})

@login_required(login_url='/login-nutricionista/')
def mis_pautas(request):
    if not request.user.es_nutri:
        messages.error(request,'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    if request.method == "POST":
        form = FormPautaAlimentaria(request.POST)
        if form.is_valid():
            # form.save()
            pass
    else:
        form = FormPautaAlimentaria()
    return render(request, 'nutricionista/mis_pautas.html',{'form':form})


class MenuDetalle(UpdateView):
    model = Menu
    fields = '__all__'
    template_name = 'nutricionista/menu_detail.html'
        