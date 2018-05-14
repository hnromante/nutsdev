from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.
@login_required(login_url='/login-superadmin/')
def inicio_superadmin(request):
    if not request.user.es_superadmin:
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login-superadmin')

    return render(request,'superadmin/index.html')