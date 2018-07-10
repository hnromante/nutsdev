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


class Atencion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE)
    motivo = models.CharField(
        max_length=2,
        choices=OPCIONES_MOTIVO,
        default='PA',
    )

    observacion = models.CharField(max_length=200)
    fecha = models.DateField(null=True, blank= True)
    hora = models.TimeField(null=True, blank= True)
    asistencia = models.BooleanField(default=False)

    def expirada(self):
        combined_date = datetime.datetime.combine(self.fecha, self.hora)
        return True if combined_date < datetime.datetime.now() else False
    def seg_a_reserva(self):
        segundos = (datetime.datetime.combine(self.fecha, self.hora) - datetime.datetime.now()).total_seconds() 
        return segundos
    def tiempo_a_la_reserva(self):

        print(datetime.datetime.now())
        print("FECHA RES")
        print(datetime.datetime.combine(self.fecha, self.hora))
        segundos = (datetime.datetime.combine(self.fecha, self.hora) - datetime.datetime.now()).total_seconds()
        print(segundos)
        minutos = segundos/60
        print(minutos)
        horas = minutos/60
        print(horas)
        dias = horas/24
        print(dias)
        if(segundos < 0):
            return 'caducada'
        if (dias >= 1):
            return 'en {} días'.format(round(dias))
        else:
            return 'en {} horas'.format(round(horas))

        
    
    
    def __str__(self):
        return 'Atención [Nutri: {} - Paci: {}]'.format(self.nutricionista.user.get_nombre_completo, self.paciente.user.get_nombre_completo)