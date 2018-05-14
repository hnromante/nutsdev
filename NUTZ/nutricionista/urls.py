from django.conf.urls import url
from nutricionista import views


urlpatterns = [
    url(r'^$', views.inicio_nutri, name='nutricionista'),
    url(r'^mis-pacientes/$', views.mis_pacientes, name='nutricionista--pacientes'),
    url(r'^calculadora/$', views.calculadora, name='nutricionista--calculadora'),
    
]
