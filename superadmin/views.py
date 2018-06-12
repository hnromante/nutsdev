from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from superadmin.models import GrupoAlimento
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import SuperAdmin
# Create your views here.
@login_required(login_url='/login-superadmin/')
def inicio_superadmin(request):
    """
    Controlador del dashboard de superadmin. Va a mostrar información relevante para los administradores del sistema.
    Va a poder modificar variables globales desde acá.
    :param request:
    :return:
    """
    if not SuperAdmin.objects.filter(user=request.user).exists() :
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-superadmin')

    return render(request,'superadmin/index.html')

def grupoAlimentosJson(request):
    """
    Controlador grupos de alimentos. Retorna en formato JSON la data de grupos de alimentos.

    :param request:
    :return:
    """
    queryset = GrupoAlimento.objects.all().values('pk', 'nombre', 'kcal_prom', 'cho_prom', 'pro_prom', 'lip_prom')
    serialized_q = json.dumps(list(queryset), cls=DjangoJSONEncoder)
    return JsonResponse(serialized_q, safe=False)


@login_required(login_url='/login-superadmin/')
def gestor_grupos_aliemntos(request):
    """
    Controlador de grupos de alimentos. Desde acá el superadmin va a poder modificar, agregar o eliminar grupos de alimentos.
    Retorna el template de gestor de grupos de alimentos
    :param request:
    :return:
    """
    return render(request, 'superadmin/gestor_grupo_alimentos.html')


@login_required(login_url='/login-superadmin/')
def gestor_aliemntos(request):
    """
    Controlador de alimentos. Desde acá el superadmin va a poder modificar, agregar o eliminar alimentos.
    Retorna el template de gestor de alimentos
    :param request:
    :return:
    """
    return render(request, 'superadmin/gestor_alimentos.html')
