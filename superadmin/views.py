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
    if not SuperAdmin.objects.filter(user=request.user).exists() :
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-superadmin')

    return render(request,'superadmin/index.html')

def grupoAlimentosJson(request):
    # grupo_alimentos = GrupoAlimento.objects.all()
    # return JsonResponse(serializers.serialize('json', list(grupo_alimentos)), safe=False, fields=('nombre','kcal_prom'))
    queryset = GrupoAlimento.objects.all().values('nombre','kcal_prom', 'cho_prom', 'pro_prom', 'lip_prom')
    serialized_q = json.dumps(list(queryset), cls=DjangoJSONEncoder)
    return JsonResponse(serialized_q, safe=False)


@login_required(login_url='/login-superadmin/')
def gestor_grupos_aliemntos(request):
    return render(request, 'superadmin/gestor_grupo_alimentos.html')


@login_required(login_url='/login-superadmin/')
def gestor_aliemntos(request):
    return render(request, 'superadmin/gestor_alimentos.html')
