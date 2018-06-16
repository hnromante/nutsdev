from django.contrib import admin
from .models import (
    AntecedentesAlimentarios,
    CalculadoraPiramidal,
    FichaBioquimica,
    FichaGeneral,
    FichaNutricional,
    Paciente
)

admin.site.register(AntecedentesAlimentarios)
admin.site.register(CalculadoraPiramidal)
admin.site.register(FichaBioquimica)
admin.site.register(FichaGeneral)
admin.site.register(FichaNutricional)
admin.site.register(Paciente)
