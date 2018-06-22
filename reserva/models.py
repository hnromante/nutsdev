###################
#MODELOS
###################
from django.db import models
from paciente.models import Paciente
from nutricionista.models import Nutricionista
from django.utils import timezone
import datetime

OPCIONES_MOTIVO= (
    ('PA', 'Primera atención'),
    ('CO', 'Control'),
    ('UA', 'Última atención'),
)
OPCIONES_ESTADO = (
    ('PE', 'Pendiente'),
    ('CA', 'Cancelada'),
    ('CO', 'Completada'),
    ('SA', 'Sin asistencia')
)

class Atencion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE)
    motivo = models.CharField(
        max_length=2,
        choices=OPCIONES_MOTIVO,
        default='PA',
    )
    estado = models.CharField(
        max_length=2,
        choices=OPCIONES_ESTADO,
        default='PE',
    )
    observacion = models.CharField(max_length=200)
    fecha = models.DateField(null=True, blank= True)
    hora = models.TimeField(null=True, blank= True)


    def expirada(self):
        combined_date = datetime.datetime.combine(self.fecha, self.hora)
        return True if combined_date < datetime.datetime.now() else False
    
    def tiempo_a_la_reserva(self):
        print("NOW")
        print(datetime.datetime.now())
        print("FECHA RES")
        print(datetime.datetime.combine(self.fecha, self.hora))
        segundos = (datetime.datetime.now() - datetime.datetime.combine(self.fecha, self.hora)).total_seconds()
        print(segundos)
        minutos = segundos/60
        print(minutos)
        horas = minutos/60
        print(horas)
        dias = horas/60
        print(horas)
        return datetime.datetime.now() - datetime.datetime.combine(self.fecha, self.hora)
    
    
    def __str__(self):
        return 'Atención [Nutri: {} - Paci: {}]'.format(self.nutricionista.user.get_nombre_completo, self.paciente.user.get_nombre_completo)