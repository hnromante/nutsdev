from django.db import models

# Create your models here.
class TipoAlimento(models.Model):
    nombre = models.CharField(max_length=50)
    cho_prom = models.IntegerField()
    lipidos_prom = models.IntegerField()
    proteinas_prom = models.IntegerField()
    azucares_prom = models.IntegerField()

class Alimento(models.Model):
    nombre = models.CharField(max_length=50)
    cho = models.IntegerField()
    lipidos = models.IntegerField()
    proteinas = models.IntegerField()
    azucares = models.IntegerField()
    tipo_alimento = models.ForeignKey(TipoAlimento, on_delete=models.CASCADE, related_name='aliemntos')