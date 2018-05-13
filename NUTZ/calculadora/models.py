from django.db import models

# Create your models here.

class GrupoAlimento (models.Model):
    nombre = models.CharField(max_length=30)
    kcal_prom = models.FloatField()
    def __str__(self):
        return self.nombre

class Alimento (models.Model):
    nombre = models.CharField(max_length=30)
    grupo = models.ForeignKey(GrupoAlimento,on_delete=models.CASCADE)
    kcal = models.FloatField(default=140)

    def __str__(self):
        return self.nombre
    

class Calculadora (models.Model):
    alimentos = models.ManyToManyField(Alimento)
    porcion = models.IntegerField()
    kcal_ideal = models.FloatField()
    #alimentos = models.ManyToManyField(GrupoAlimento)


