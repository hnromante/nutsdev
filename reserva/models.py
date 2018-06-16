###################
#MODELOS
###################
from django.db import models
from paciente.models import Paciente
from nutricionista.models import Nutricionista

class Atencion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    nutricionista = models.ForeignKey(Nutricionista, on_delete=models.CASCADE)
    OPCIONES_MOTIVO= (
    ('PA', 'Primera atención'),
    ('CO', 'Control'),
    ('UA', 'Última atención'),
    )
    motivo = models.CharField(
        max_length=2,
        choices=OPCIONES_MOTIVO,
        default='PA',
        )
    observacion = models.CharField(max_length=200)
    fecha = models.DateField(null=True, blank= True)
    hora = models.TimeField(null=True, blank= True)
    
    

    def __str__(self):
        return 'Atención [Nutri: {} - Paci: {}]'.format(self.nutricionista.user.get_nombre_completo, self.paciente.user.get_nombre_completo)