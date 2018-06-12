from django.shortcuts import render
from nutricionista.models import Nutricionista, Menu, PautaAlimentaria
from django.views.generic.list import ListView
from paciente.models import Paciente, CalculadoraPiramidal
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
import json
from django.utils import timezone
from django.urls import reverse
def calculadora(request):
    return render(request,template_name='nutricionista/calculadora.html')

@login_required(login_url='/login-nutricionista/')
def inicio_nutri(request):
    """
    Controlador del dashboard del nutricionista. Entrega información general útil para el paciente,
    como el número de pacietes asociados a la nutricionista y estadísticas.
    Retorna el template de dashboard.
    :param request:
    :return:
    """
    if not request.user.es_nutri:
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa página')
        return HttpResponseRedirect('/login-nutricionista')
    numero_pacientes = len(Paciente.objects.filter(nutricionista=request.user.nutricionista))
    pacientes_normal = len(Paciente.objects.filter(nutricionista=request.user.nutricionista, diagnostico_peso='Peso normal'))
    pacientes_bajo = len(Paciente.objects.filter(nutricionista=request.user.nutricionista, diagnostico_peso='Bajo peso'))
    pacientes_sobrepeso = len(Paciente.objects.filter(nutricionista=request.user.nutricionista, diagnostico_peso='Sobrepeso'))
    pacientes_obesidad1 = len(Paciente.objects.filter(nutricionista=request.user.nutricionista, diagnostico_peso='Obesidad grado 1'))
    pacientes_obesidad2 = len(Paciente.objects.filter(nutricionista=request.user.nutricionista, diagnostico_peso='Obesidad grado 2'))
    pacientes_obesidad_morbida = len(Paciente.objects.filter(nutricionista=request.user.nutricionista, diagnostico_peso='Obesidad mórbida'))
    print(pacientes_obesidad1)
    return render(request,'nutricionista/index.html', {'numero_pacientes':numero_pacientes, 'pacientes_normal':pacientes_normal, 'pacientes_bajo':pacientes_bajo,
                                                        'pacientes_sobrepeso':pacientes_sobrepeso, 'pacientes_obesidad1':pacientes_obesidad1, 'pacientes_obesidad2':pacientes_obesidad2,
                                                        'pacientes_obesidad_morbida':pacientes_obesidad_morbida})


@login_required(login_url='/login-nutricionista/')
def mis_pacientes(request):
    """
    Controlador Muestra un listado de los pacientes asociados a la nutricionita.
    Retorna el template de pacientes.html.
    Además filtra cuando se presiona el botón de búsqueda por el rut correspondiente.
    :param request:
    :return:
    """
    if request.method == 'POST':
        rut = request.POST['busqueda']
        pacientes = Paciente.objects.filter(nutricionista=request.user.nutricionista, user__rut = rut)
        print(pacientes)
        return render(request, 'nutricionista/pacientes.html', {'pacientes':pacientes})

    if not request.user.es_nutri:
        messages.warning(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    context = dict()
    pacientes = Paciente.objects.filter(nutricionista=request.user.nutricionista)

    return render(request, 'nutricionista/pacientes.html', {'pacientes':pacientes})


@login_required(login_url='/login-nutricionista/')
def paciente_detalle(request, pk, ficha=''):
    """
    Controlador Detalle del paciente, recibe como parámetros el PK o ID del paciente (lanza un 404 si no se encuentra).
    Recibe además una ficha que va a mostrar un formulario específico. Las fichas válidas son: (usuario, general,
    antecedentes, bioquimica, calculadora y recomendaciones)
    Retorna el template de paciente detalle por defecto, pero renderiza las ficahs dependiendo del parametro enviado por URL.
    :param request:
    :param pk:
    :param ficha:
    :return:
    """
    
    if not request.user.es_nutri:
        messages.warning(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    paciente = Paciente.objects.get(pk=pk) #CAMBIAR POR GET OBJECT OR 404
    

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

            if form_paciente.is_valid():
                form_paciente.save()
                messages.success(request, "Información actualizada")

        else:
            form_paciente = FormFichaGeneral(instance=paciente)
        return render(request, 'nutricionista/paciente_ficha_general.html', {'form_paciente': form_paciente, 'paciente':paciente})

    elif ficha == 'usuario':
        if request.method == 'POST':
            form_usuario = FormUsuario(request.POST, instance=paciente.user)
            if form_usuario.is_valid():
                form_usuario.save()
                messages.success(request, "Información de usuario actualizada")
                return HttpResponseRedirect('/nutricionista/mis-pacientes/{}/'.format(paciente.pk))
        else:
            form_usuario = FormUsuario(instance=paciente.user) 
        return render(request, 'nutricionista/paciente_ficha_usuario.html', {'form_usuario': form_usuario, 'paciente':paciente})

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
        calculadora = CalculadoraPiramidal.objects.get(paciente=paciente) if CalculadoraPiramidal.objects.filter(paciente=paciente).exists() else None
            
        if request.method == 'POST':
            datos_calculadora = json.loads(request.POST['datos_calculadora'])
            if calculadora:
                cal = CalculadoraPiramidal.objects.get(paciente=paciente)
                cal.peso_a_utilizar = datos_calculadora['peso_a_utilizar']
                cal.kcal_estado_nutricional = datos_calculadora['kcal_estado_nutricional']
                cal.total_kcal = datos_calculadora['total_kcal']
                cal.vct = datos_calculadora['vct']
                cal.grupos_porciones = datos_calculadora['grupos_porciones']
                cal.ultima_actualizacion = timezone.now()
                cal.save()
            else:
                cal = CalculadoraPiramidal.objects.create(paciente=paciente)
                cal.kcal_estado_nutricional = datos_calculadora['kcal_estado_nutricional']
                cal.peso_a_utilizar = datos_calculadora['peso_a_utilizar']  
                cal.total_kcal = datos_calculadora['total_kcal']
                cal.vct = datos_calculadora['vct']
                cal.grupos_porciones = datos_calculadora['grupos_porciones']
                cal.save()
        return render(request, 'nutricionista/paciente_calculadora.html', {'paciente':paciente, 'calculadora':calculadora})
    else:
        if request.method == 'POST':
            if request.POST['eliminar_paciente']:
                rut = paciente.user.rut
                paciente.delete()
                messages.success(request, 'Paciente con rut: {} eliminado correctamente'.format(rut))
                return HttpResponseRedirect('/nutricionista/mis-pacientes')

    
    return render(request, 'nutricionista/paciente_single.html', {'paciente':paciente})

@login_required(login_url='/login-nutricionista/')
def agregar_paciente(request):
    """
    Función que permite agregar pacientes. Asigna por defecto una password hasheada que se le envía al paciente a través de su email
    para que la pueda cambiar.
    Retorna el template de agregar paciente.
    :param request:
    :return:
    """
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
            paciente = Paciente.objects.create(user=user, nutricionista=nutricionista,
                                  )
            messages.success(request, 'Paciente creado correctamente.')
            return HttpResponseRedirect('/nutricionista/mis-pacientes/{}/usuario'.format(paciente.pk))
    else:
        form = FormAddPaciente()
    return render(request, template_name='nutricionista/pacientes_agregar.html', context={'form':form})


@login_required(login_url='/login-nutricionista/')
def mi_perfil(request):
    """
    Controlador perfil del nutricionista donde puede editar sus dato personales.
    Retorna el template de mi perfil.
    :param request:
    :return:
    """
    if not request.user.es_nutri:
        messages.error(request,'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    if request.method == "POST":
        form = FormPerfil(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Información actualizada correctamente")
    else:
        form = FormPerfil(instance=request.user)
    return render(request, 'nutricionista/perfil.html', {'form':form})


@login_required(login_url='/login-nutricionista/')
def mis_menus(request):
    """
    Controlador de Mis menus. (NO EN USO)
    Retorna el template de mis menus
    :param request:
    :return:
    """
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
    return render(request, 'nutricionista/mis_menus.html',{'form':form,
                                                            'menus':menus})

@login_required(login_url='/login-nutricionista/')
def mis_pautas(request):
    """
    Controlador de mis pautas alimentarias. (NO EN USO)
    :param request:
    :return:
    """
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
    """
    Clase que retorna el detalle en Menú.
    """
    model = Menu
    fields = '__all__'
    template_name = 'nutricionista/menu_detail.html'
    redirect_url = ''
        
