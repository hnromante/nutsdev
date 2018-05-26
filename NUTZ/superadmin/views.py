from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from superadmin.models import GrupoAlimento
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
# Create your views here.
@login_required(login_url='/login-superadmin/')
def inicio_superadmin(request):
    if not request.user.es_superadmin:
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-superadmin')

    return render(request,'superadmin/index.html')

def grupoAlimentosJson(request):
    # grupo_alimentos = GrupoAlimento.objects.all()
    # return JsonResponse(serializers.serialize('json', list(grupo_alimentos)), safe=False, fields=('nombre','kcal_prom'))
    queryset = GrupoAlimento.objects.all().values('nombre','kcal_prom', 'cho_prom', 'pro_prom', 'lip_prom')
    serialized_q = json.dumps(list(queryset), cls=DjangoJSONEncoder)
    return JsonResponse(serialized_q, safe=False)