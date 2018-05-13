from django.shortcuts import render
from nutricionista.models import Nutricionista
from django.views.generic.list import ListView
from paciente.models import Paciente
from django.apps import apps
from .forms import (
    FormAddPaciente,
)
from django.shortcuts import get_object_or_404
from django.contrib import messages

from alimento.models import TipoAlimento, Alimento
# Create your views here.
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

def index(request):
    return render(request,template_name='nutricionista/index.html')

def dashboard(request):
    return render(request,template_name='nutricionista/dashboard.html')

def calculadora(request):
    return render(request,template_name='nutricionista/calculadora.html')

#La nutricionista en el inicio, va a poder ver un formulario para
#agregar paciente y listarlos.
#INGRESA PACIENTE FORMULARIO -> SE VALIDA EN LA F.B.V. -> SE DEVUELVE UNA LISTA ACTUALIZADA
@login_required(login_url='/login/')
def inicio_nutri(request):
    if not request.user.es_nutri:
        messages.add_message(request, messages.INFO, 'Usted no tiene los permisos para visitar esa pagina')
        return HttpResponseRedirect('/login')
    if request.method == "POST":
        form_add_paciente = FormAddPaciente(request.POST)
        if form_add_paciente.is_valid():
            user = get_auth_user()
            nutricionista = user.nutricionista 
            email = form_add_paciente.cleaned_data['email']
            rut = form_add_paciente.cleaned_data['rut']
            nutricionista = get_object_or_404(Nutricionista, pk=5)
            paciente = nutricionista.crear_paciente(email=email,rut=rut, es_paciente=True, es_nutri=False, password='password123') #rut, email, law e
            print("Paciente creado desde el form")
            messages.add_message(request, messages.INFO, 'Paciente creado correctamente!')

    else:
        form_add_paciente = FormAddPaciente()
    context = dict()
    context['form'] = form_add_paciente

    return render(request,'nutricionista/index.html', context)

class PacienteListView(ListView):
    model = Paciente

    template_name = 'nutricionista/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    

class TipoAlimentoList(ListView):
    model = TipoAlimento
    template_name = 'nutricionista/alimentos.html'

class AlimentoList(ListView):
    model = Alimento
    template_name = 'nutricionista/tipoalimento.html'

class TipoAlimentoCreate(ListView):
    model = TipoAlimento
    template_name = 'nutricionista/crearalimento.html'

class AlimentoCreate(ListView):
    model = Alimento
    template_name = 'nutricionista/creartipoalimento.html'