from django.db import models

# Create your models here.

class Tema(models.Model):
    titulo = models.CharField(max_length=254)


class Faq(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    pregunta = models.CharField(max_length=254)
    respuesta = models.CharField(max_length=254)
