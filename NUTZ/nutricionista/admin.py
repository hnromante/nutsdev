from django.contrib import admin
from .models import Nutricionista, PautaAlimentaria, Comida
# Register your models here.


class PautaAlimentariaManager(admin.ModelAdmin):
    model = PautaAlimentaria
    filter_horizontal = ('comidas',) #If you don't specify this, you will get a multiple select widget.

class ComidaManager(admin.ModelAdmin):
    model = Comida
    filter_horizontal = ('alimentos',) #If you don't specify this, you will get a multiple select widget.

admin.site.register(Nutricionista)
admin.site.register(Comida, ComidaManager)
admin.site.register(PautaAlimentaria, PautaAlimentariaManager)