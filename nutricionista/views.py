from django.shortcuts import render
from nutricionista.models import Nutricionista, Menu, PautaAlimentaria
from django.views.generic.list import ListView
from paciente.models import Paciente
from django.apps import apps
from .forms import (
    FormAddPaciente,
    FormPerfil,
    FormMenu,
    FormPautaAlimentaria,
    FormFichaNutricional,
    FormFichaBioquimica,
    FormFichaGeneral,
    FormAntecedentesAlimentarios,
    FormUsuario
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
from django.http import JsonResponse

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

    return render(request, 'nutricionista/pacientes.html', {'pacientes':pacientes})


@login_required(login_url='/login-nutricionista/')
def paciente_detalle(request, pk, ficha=''):
    paciente = Paciente.objects.get(pk=pk)
    if not request.user.es_nutri:
        messages.warning(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')

    if ficha == 'nutricional':
        if request.method == 'POST':
            form = FormFichaNutricional(request.POST, instance=paciente)
            if form.is_valid():
                form.save()
                messages.success(request, "Información actualizada")
        else:
            form = FormFichaNutricional(instance=paciente)
        return render(request, 'nutricionista/paciente_ficha_nutricional.html', {'form': form, 'paciente':paciente})
    
    elif ficha == 'bioquimica':
        if request.method == 'POST':
            form = FormFichaBioquimica(request.POST, instance=paciente)
            if form.is_valid():
                form.save()
                messages.success(request, "Información actualizada")
        else:
            form = FormFichaBioquimica(instance=paciente)
        return render(request, 'nutricionista/paciente_ficha_bio.html', {'form': form, 'paciente':paciente})
    
    elif ficha == 'general':
        if request.method == 'POST':
            form_paciente = FormFichaGeneral(request.POST, instance=paciente)
            form_usuario = FormUsuario(request.POST, instance=request.user)
            if form_paciente.is_valid():
                form_paciente.save()
                messages.success(request, "Información actualizada")
            elif form_usuario.is_valid():
                form_usuario.save()
                print("dddd")
                messages.success(request, "Información actualizada")
        else:
            form_paciente = FormFichaGeneral(instance=paciente)
            form_usuario = FormUsuario(instance=request.user) 
        return render(request, 'nutricionista/paciente_ficha_general.html', {'form_paciente': form_paciente, 'form_usuario': form_usuario, 'paciente':paciente})

    elif ficha == 'recomendaciones':
        return render(request, 'nutricionista/paciente_recomendaciones.html', {'paciente':paciente})

    elif ficha == 'antecedentes':
        if request.method == 'POST':
            form = FormAntecedentesAlimentarios(request.POST, instance=paciente)
            if form.is_valid():
                form.save()
                messages.success(request, "Información actualizada")
        else:
            form = FormAntecedentesAlimentarios(instance=paciente)
        return render(request, 'nutricionista/paciente_antecedentes.html', {'form': form, 'paciente':paciente})

    elif ficha == 'calculadora':
        return render(request, 'nutricionista/paciente_calculadora.html', {'paciente':paciente})
    else:
        pass
    
    return render(request, 'nutricionista/paciente_single.html', {'paciente':paciente})

@login_required(login_url='/login-nutricionista/')
def agregar_paciente(request):
    if not request.user.es_nutri:
        messages.success(request, 'Usted no tiene los permisos para visitar esa pagina')
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
                                  )
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
        form = FormPerfil(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
    else:
        print("not valid")
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
    redirect_url = ''
        

