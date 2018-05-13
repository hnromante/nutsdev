from django.contrib import admin
from faq.models import (
    Tema,
    Faq
)
# Register your models here.

admin.site.register(Tema)
admin.site.register(Faq)