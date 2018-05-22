from django.contrib import admin
from .models import Nutricionista, PautaAlimentaria, Menu
# Register your models here.


class PautaAlimentariaManager(admin.ModelAdmin):
    model = PautaAlimentaria
    filter_horizontal = ('menus',) #If you don't specify this, you will get a multiple select widget.

class ComidaManager(admin.ModelAdmin):
    model = Menu
    filter_horizontal = ('alimentos',) #If you don't specify this, you will get a multiple select widget.

admin.site.register(Nutricionista)
admin.site.register(Menu, ComidaManager)
admin.site.register(PautaAlimentaria, PautaAlimentariaManager)