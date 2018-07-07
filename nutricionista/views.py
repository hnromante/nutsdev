from django.shortcuts import render
from nutricionista.models import Nutricionista
from django.views.generic.list import ListView
from paciente.models import (
    AntecedentesAlimentarios,
    CalculadoraPiramidal,
    FichaBioquimica,
    FichaGeneral,
    FichaNutricional,
    Paciente
)
from superadmin.models import GrupoAlimento
from recomendacion.models import Recomendacion
from django.apps import apps
from nutricionista.forms import FormPerfil
from reserva.forms import FormCrearAtencion
from reserva.models import Atencion
from paciente.forms import (
    FormAddPaciente,
    FormFichaNutricional,
    FormFichaBioquimica,
    FormFichaGeneral,
    FormAntecedentesAlimentarios,
    FormUsuario
)
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
from datetime import date
import datetime
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
    numero_pacientes = Paciente.objects.filter(nutricionista=request.user.nutricionista).count()
    hoy = date.today()
    atenciones_hoy = Atencion.objects.filter(nutricionista=request.user.nutricionista, fecha__day=hoy.day).count()
    atenciones_tomorrow = Atencion.objects.filter(nutricionista=request.user.nutricionista, fecha__day=hoy.day+1).count()
    proxima_atencion = Atencion.objects.filter(nutricionista=request.user.nutricionista).order_by('fecha').last()
    # pacientes_normal = Paciente.objects.filter(nutricionista=request.user.nutricionista, fichanutricional__diagnostico_peso='Peso normal').count()
    # pacientes_bajo = Paciente.objects.filter(nutricionista=request.user.nutricionista, fichanutricional__diagnostico_peso='Bajo Peso').count()
    # pacientes_sobrepeso = Paciente.objects.filter(nutricionista=request.user.nutricionista, fichanutricional__diagnostico_peso='Sobrepeso').count()
    # pacientes_obesidad1 = Paciente.objects.filter(nutricionista=request.user.nutricionista, fichanutricional__diagnostico_peso='Obesidad grado 1').count()
    # pacientes_obesidad2 = Paciente.objects.filter(nutricionista=request.user.nutricionista, fichanutricional__diagnostico_peso='Obesidad grado 2').count()
    # pacientes_obesidad_morbida = Paciente.objects.filter(nutricionista=request.user.nutricionista, fichanutricional__diagnostico_peso='Obesidad mórbida').count()
    atenciones = Atencion.objects.filter(nutricionista=request.user.nutricionista).order_by('fecha')[:2]
    if proxima_atencion.expirada():
        proxima_atencion = None
    return render(request,'nutricionista/index.html', { 'atenciones':atenciones,
                                                        'atenciones_hoy':atenciones_hoy,
                                                        'proxima_atencion': proxima_atencion,
                                                        'atenciones_tomorrow': atenciones_tomorrow,
                                                        'numero_pacientes':numero_pacientes, 
                                                        # 'pacientes_normal':pacientes_normal,
                                                        # 'pacientes_bajo':pacientes_bajo, 'pacientes_sobrepeso':pacientes_sobrepeso, 
                                                        # 'pacientes_obesidad1':pacientes_obesidad1, 'pacientes_obesidad2':pacientes_obesidad2,
                                                        # 'pacientes_obesidad_morbida':pacientes_obesidad_morbida
                                                        })


@login_required(login_url='/login-nutricionista/')
def mis_pacientes(request):
    """
    Controlador Muestra un listado de los pacientes asociados a la nutricionita.
    Retorna el template de pacientes.html.
    Además filtra cuando se presiona el botón de búsqueda por el rut correspondiente.
    :param request:
    :return:
    """
    if not request.user.es_nutri:
        messages.warning(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    
    if request.method == 'POST':
        rut = request.POST['busqueda']
        pacientes = Paciente.objects.filter(nutricionista=request.user.nutricionista, user__rut = rut)

        return render(request, 'nutricionista/pacientes.html', {'pacientes':pacientes})
    pacientes_list = Paciente.objects.filter(nutricionista=request.user.nutricionista)
    pagination = Paginator(pacientes_list, 4)
    page = request.GET.get('page')
    pacientes = pagination.get_page(page)

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
    proxima_atencion = Atencion.objects.filter(paciente=paciente, nutricionista=request.user.nutricionista).order_by('-fecha').last()

    if ficha == 'nutricional':
        ficha_nutricional = FichaNutricional.objects.get(paciente=paciente) if FichaNutricional.objects.filter(paciente=paciente).exists() else FichaNutricional.objects.create(paciente=paciente)
        if request.method == 'POST':
            form = FormFichaNutricional(request.POST, instance=ficha_nutricional)
            if form.is_valid():
                form.save()
                messages.success(request, "Información actualizada")
        else:
            form = FormFichaNutricional(instance=ficha_nutricional)
        return render(request, 'nutricionista/paciente_ficha_nutricional.html', {'form': form, 'paciente':paciente})
    
    elif ficha == 'bioquimica':
        ficha_bioquimica = FichaBioquimica.objects.get(paciente=paciente) if FichaBioquimica.objects.filter(paciente=paciente).exists() else FichaBioquimica.objects.create(paciente=paciente)
        if request.method == 'POST':
            form = FormFichaBioquimica(request.POST, instance=ficha_bioquimica)
            if form.is_valid():
                form.save()
                messages.success(request, "Información actualizada")
        else:
            form = FormFichaBioquimica(instance=ficha_bioquimica)
        return render(request, 'nutricionista/paciente_ficha_bio.html', {'form': form, 'paciente':paciente})
    
    elif ficha == 'general':
        ficha_general = FichaGeneral.objects.get(paciente=paciente) if FichaGeneral.objects.filter(paciente=paciente).exists() else FichaGeneral.objects.create(paciente=paciente)

        if request.method == 'POST':
            form = FormFichaGeneral(request.POST, request.FILES,  instance=ficha_general)
            if form.is_valid():
                ficha_general.imagen = form.cleaned_data['imagen']
                print(request.FILES)
                print(ficha_general)
                ficha_general.save()
                form.save()
                messages.success(request, "Información actualizada")

        else:
            form = FormFichaGeneral(instance=ficha_general)
        return render(request, 'nutricionista/paciente_ficha_general.html', {'form': form, 'paciente':paciente})

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
        ficha_antecedentes = AntecedentesAlimentarios.objects.get(paciente=paciente) if AntecedentesAlimentarios.objects.filter(paciente=paciente).exists() else AntecedentesAlimentarios.objects.create(paciente=paciente)
        if request.method == 'POST':
            form = FormAntecedentesAlimentarios(request.POST, instance=ficha_antecedentes)
            if form.is_valid():
                form.save()
                messages.success(request, "Información actualizada")
        else:
            form = FormAntecedentesAlimentarios(instance=ficha_antecedentes)
        return render(request, 'nutricionista/paciente_antecedentes.html', {'form': form, 'paciente':paciente})

    elif ficha == 'calculadora':
        # calculadora = CalculadoraPiramidal.objects.get(paciente=paciente) if CalculadoraPiramidal.objects.filter(paciente=paciente).exists() else None
        calculadora = CalculadoraPiramidal.objects.get(paciente=paciente) if CalculadoraPiramidal.objects.filter(paciente=paciente).exists() else CalculadoraPiramidal.objects.create(paciente=paciente)    
        if request.method == 'POST':
            datos_calculadora = json.loads(request.POST['datos_calculadora'])
            calculadora.peso_a_utilizar = datos_calculadora['peso_a_utilizar']
            calculadora.kcal_estado_nutricional = datos_calculadora['kcal_estado_nutricional']
            calculadora.total_kcal = datos_calculadora['total_kcal']
            calculadora.vct = datos_calculadora['vct']
            calculadora.grupos_porciones = datos_calculadora['grupos_porciones']
            calculadora.ultima_actualizacion = timezone.now()
            calculadora.save()
        return render(request, 'nutricionista/paciente_calculadora.html', {'paciente':paciente, 'calculadora':calculadora})
    
    form = FormCrearAtencion()
    if request.method == 'POST':
        if request.POST['agendar']:
            atencion = Atencion.objects.create(paciente=paciente, nutricionista=request.user.nutricionista)
            form = FormCrearAtencion(request.POST, instance=atencion)
            if form.is_valid():
                form.save()
                messages.success(request, "Próxima atención creada!")
                return render(request, 'nutricionista/paciente_single.html', {'paciente':paciente, 'proxima_atencion':atencion, 'form':form})
            else:
                print("iNVALIDO")
    return render(request, 'nutricionista/paciente_single.html', {'paciente':paciente, 'proxima_atencion':proxima_atencion, 'form':form})

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
            user = User.objects.create_user(rut=form.cleaned_data['rut'], email= form.cleaned_data['email'], 
                                                password='password123', es_paciente=True, es_nutri=False)
            paciente = Paciente.objects.create(user=user, nutricionista=nutricionista)
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
            form.save()
            messages.success(request, "Información actualizada correctamente")
    else:
        form = FormPerfil(instance=request.user)
    return render(request, 'nutricionista/perfil.html', {'form':form})


@login_required(login_url='/login-nutricionista/')
def atenciones(request):
    """
    Controlador perfil del nutricionista donde puede editar sus dato personales.
    Retorna el template de mi perfil.
    :param request:
    :return:
    """
    if not request.user.es_nutri:
        messages.error(request,'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')
    atenciones_list = Atencion.objects.filter(nutricionista=request.user.nutricionista ,fecha__gte=datetime.datetime.now()).order_by('fecha')
    pagination = Paginator(atenciones_list, 4)
    page = request.GET.get('page')
    atenciones = pagination.get_page(page)
    
    return render(request, 'nutricionista/atenciones.html', {'atenciones':atenciones})

@login_required(login_url='/login-nutricionista/')
def atenciones_historial(request):
    """
    Controlador perfil del nutricionista donde puede editar sus dato personales.
    Retorna el template de mi perfil.
    :param request:
    :return:
    """
    if not request.user.es_nutri:
        messages.error(request,'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-nutricionista')

    atenciones_expiradas_list = Atencion.objects.filter(nutricionista=request.user.nutricionista ,fecha__lt=datetime.datetime.now()).order_by('fecha')
    pagination = Paginator(atenciones_expiradas_list, 4)
    page = request.GET.get('page')
    atenciones_expiradas = pagination.get_page(page)
    return render(request, 'nutricionista/atenciones_historial.html', {'atenciones_expiradas':atenciones_expiradas})


@login_required(login_url='/login-nutricionista/')
def atencion_single(request, pk):
    """
    Controlador perfil del nutricionista donde puede editar sus dato personales.
    Retorna el template de mi perfil.
    :param request:
    :return:
    """
    if not request.user.es_nutri:
        messages.error(request,'Usted no tiene los permisos para visitar esta página')
        return HttpResponseRedirect('/login-nutricionista')
    atencion = Atencion.objects.get(pk=pk)
    print(atencion.paciente)
    print(atencion.nutricionista)
    form = FormCrearAtencion(instance=atencion)
    if request.method == 'POST':
        if request.POST['modificar_reserva']:
            form = FormCrearAtencion(request.POST, instance=atencion)
            if form.is_valid():
                form.save()
                messages.success(request, "Reserva modificada")
    return render(request, 'nutricionista/atencion_single.html', {'atencion':atencion, 'form':form})


@login_required(login_url='/login-nutricionista/')
def atencion_eliminar(request, pk):
    if not request.user.es_nutri:
        messages.error(request,'Usted no tiene los permisos para visitar esta página')
        return HttpResponseRedirect('/login-nutricionista')

    atencion = Atencion.objects.get(pk=pk)
    if request.POST['eliminar_reserva']:
        atencion.delete()
    return HttpResponseRedirect('/nutricionista/atenciones')


"""
API
"""    
"""
Caltura los alimentos asociados a un grupo de alimentos
"""
def capturarAlimentosDeGrupo(pk_grupo):
    grupo = GrupoAlimento.objects.get(pk=pk_grupo)
    alimentos = grupo.alimento_set.all()
    lista_alimentos = list()
    for alimento in alimentos:
        data = dict()
        data['pk'] = alimento.pk
        data['nombre'] = alimento.nombre
        data['kcal'] = alimento.kcal
        lista_alimentos.append(data)
    return lista_alimentos

def recomendacion_paciente(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    if not Recomendacion.objects.filter(paciente=paciente).exists():
        return JsonResponse({'pk_paciente': pk, 'tiene_recomendacion': False}, safe=False)
    else:
        data = dict()
        recomendacion = Recomendacion.objects.get(paciente=paciente)
        calculadora = CalculadoraPiramidal.objects.get(paciente=paciente)
        grupos_permitidos = calculadora.grupos_porciones
        if grupos_permitidos:
            for grupos_permitido in grupos_permitidos:
                grupos_permitido['alimentos'] =  capturarAlimentosDeGrupo(grupos_permitido['pk'])
            data['grupos_permitidos'] = calculadora.grupos_porciones
        else:
            data['grupos_permitidos'] = None
        data['tiene_recomendacion'] = True
        data['pk'] = recomendacion.pk
        data['paciente'] = recomendacion.paciente.pk
        data['observacion'] = recomendacion.observacion
        data['comidas'] = recomendacion.comidas
        data['total_kcal'] = calculadora.total_kcal
        print(calculadora.total_kcal)
        print(recomendacion.comidas)
        return JsonResponse(data, safe=False)

def recomendacion_paciente_save(request, pk):
    if request.method == 'POST':
        data_recomendacion = json.loads(request.POST['recomendacion'])
        recomendacion = Recomendacion.objects.get(pk=data_recomendacion['pk'])
        recomendacion.grupos_permitidos = data_recomendacion['grupos_permitidos']
        recomendacion.grupos_permitidos_aux = data_recomendacion['grupos_permitidos_aux']
        recomendacion.total_kcal = data_recomendacion['total_kcal']
        recomendacion.comidas = data_recomendacion['comidas']
        recomendacion.observacion = data_recomendacion['observacion']
        recomendacion.save()
        return HttpResponse("success")
    return HttpResponse("error")


    
"""
    elif ficha == 'calculadora':
        # calculadora = CalculadoraPiramidal.objects.get(paciente=paciente) if CalculadoraPiramidal.objects.filter(paciente=paciente).exists() else None
        calculadora = CalculadoraPiramidal.objects.get(paciente=paciente) if CalculadoraPiramidal.objects.filter(paciente=paciente).exists() else CalculadoraPiramidal.objects.create(paciente=paciente)    
        if request.method == 'POST':
            datos_calculadora = json.loads(request.POST['datos_calculadora'])
            calculadora.peso_a_utilizar = datos_calculadora['peso_a_utilizar']
            calculadora.kcal_estado_nutricional = datos_calculadora['kcal_estado_nutricional']
            calculadora.total_kcal = datos_calculadora['total_kcal']
            calculadora.vct = datos_calculadora['vct']
            calculadora.grupos_porciones = datos_calculadora['grupos_porciones']
            calculadora.ultima_actualizacion = timezone.now()
            calculadora.save()
        return render(request, 'nutricionista/paciente_calculadora.html', {'paciente':paciente, 'calculadora':calculadora})
"""

def recomendacion_paciente_crear(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    Recomendacion.objects.create(paciente=paciente)
    return JsonResponse({'pk_paciente': pk, 'tiene_recomendacion': False}, safe=False)