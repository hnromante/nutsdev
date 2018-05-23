from django.conf.urls import url
from nutricionista import views
from django.urls import path

urlpatterns = [
    url(r'^$', views.inicio_nutri, name='nutricionista'),
    url(r'^perfil/$', views.mi_perfil, name='perfil'),
    url(r'^mis-pacientes/$', views.mis_pacientes, name='pacientes'),
    url(r'^mis-pacientes/(?P<pk>\d+)/$', views.paciente_detalle, name='paciente-detalle'),
    url(r'^mis-pacientes/(?P<pk>\d+)/(?P<ficha>\w+)$', views.paciente_detalle, name='paciente-detalle-ficha'),
    url(r'^agregar-pacientes/$', views.agregar_paciente, name='pacientes-agregar'),
    url(r'^calculadora/$', views.calculadora, name='calculadora'),
    url(r'^mis-menus/$', views.mis_menus, name='mis-menus'),
    url(r'^mis-menus/(?P<pk>\d+)/$', views.MenuDetalle.as_view(), name='menu-detalle'),
    url(r'^mis-pautas/$', views.mis_pautas, name='mis-pautas'),
]

