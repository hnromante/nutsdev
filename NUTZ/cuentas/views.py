from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from cuentas.models import User
from .forms import (
    FormRegNutri,
)


# Create your views here.

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is None:
            messages.add_message(request, messages.INFO, 'Email o contraseña incorrectos')
        else:
            django_login(request, user)
            return HttpResponseRedirect("/nutricionista")
    return render(request, template_name='login.html')


def logout (request):
    django_logout(request)
    return HttpResponseRedirect('/')


######Revisar con HUGO MAÑANA#########

def registro(request):  
    form = FormRegNutri()
    if request.method == 'POST':
        form = FormRegNutri(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            user = User.objects.create_user(rut=rut,email=email,es_paciente=False, es_nutri=True,password=password)
            django_login(request, user)
            return HttpResponseRedirect("/nutricionista")
    context = dict()
    context['form'] = form    
    return render(request,template_name='registro_nutri.html', context=context)

def inicio(request):
    
    return render(request,template_name='inicio.html')


#FUNCIONES
# def crear_usuario_nutricionista(form):
#     email = form.cleaned_data['email']
#     rut = form.cleaned_data['rut']
#     password = form.cleaned_data['password']
#     user = User.objects.create_user(rut=rut,email=email,es_paciente=False, es_nutri=True,password=password)
#     form.save()
#     return user