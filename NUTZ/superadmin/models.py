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
    cho_prom = models.IntegerField()
    pro_prom = models.IntegerField()
    lip_prom = models.IntegerField()
    azu_prom = models.IntegerField()

    def __str__(self):
        return self.nombre

class Alimento(models.Model):
    nombre = models.CharField(max_length=50)
    cho = models.IntegerField()
    pro = models.IntegerField()
    lip = models.IntegerField()
    azu = models.IntegerField()
    grupo_alimento = models.ForeignKey(GrupoAlimento, on_delete=models.CASCADE)
    porcion = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre
