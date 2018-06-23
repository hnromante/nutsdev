from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as django_login, logout as django_logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from cuentas.models import User
from nutricionista.models import Nutricionista
from .forms import (
    FormRegNutri,
)
from django.urls import reverse

# Create your views here.
def soypaciente(request):

    return render(request, template_name='cuentas/soypaciente.html')


def soynutricionista(request):

    return render(request, template_name='cuentas/soynutricionista.html')


def login_nutri(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is None:
            messages.error(request,'Email o contraseña incorrectos')
        else:
            django_login(request, user)
            return HttpResponseRedirect("/nutricionista")
    return render(request, template_name='cuentas/login_nutri.html')


def login_superadmin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is None:
            messages.add_message(request, messages.INFO, 'Email o contraseña incorrectos')
        else:
            django_login(request, user)
            return HttpResponseRedirect("/superadmin")
    return render(request, template_name='cuentas/login_superadmin.html')


def login_paci(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is None:
            messages.add_message(request, messages.INFO, 'Email o contraseña incorrectos')
        else:
            django_login(request, user)
            return HttpResponseRedirect("/paciente")
    return render(request, template_name='cuentas/login_paci.html')


def logout (request):
    django_logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return HttpResponseRedirect(reverse('login-nutricionista'))



def registro_nutri(request):  
    form = FormRegNutri()
    if request.method == 'POST':
        form = FormRegNutri(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            user = User.objects.create_user(rut=rut,email=email,es_paciente=False, es_nutri=True,password=password)
            Nutricionista.objects.create(user=user)
            django_login(request, user)
            return HttpResponseRedirect("/nutricionista")
    context = dict()
    context['form'] = form    
    return render(request,template_name='registro_nutri.html', context=context)

def inicio(request):
    
    return render(request,template_name='cuentas/inicio.html')


#FUNCIONES
# def crear_usuario_nutricionista(form):
#     email = form.cleaned_data['email']
#     rut = form.cleaned_data['rut']
#     password = form.cleaned_data['password']
#     user = User.objects.create_user(rut=rut,email=email,es_paciente=False, es_nutri=True,password=password)
#     form.save()
#     return user