from django.db import models
from cuentas.models import User
# Create your models here.
class SuperAdmin(models.Model):
    """
    Este es el modelo que v a tener control sobre todos los parametros cambiantes de la aplicacion NUTZ
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class GrupoAlimento(models.Model):
    nombre = models.CharField(max_length=50)
    kcal_prom = models.FloatField()
    cho_prom = models.FloatField()
    pro_prom = models.FloatField()
    lip_prom = models.FloatField()
    azu_prom = models.FloatField()
   

    def __str__(self):
        return self.nombre

class Alimento(models.Model):
    nombre = models.CharField(max_length=50)
    kcal = models.FloatField()
    cho = models.FloatField()
    pro = models.FloatField()
    lip = models.FloatField()
    azu = models.FloatField()
    grupo_alimento = models.ForeignKey(GrupoAlimento, on_delete=models.CASCADE)
    porcion = models.FloatField(default=1)

    def __str__(self):
        return self.nombre
