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
    url(r'^atenciones/$', views.atenciones, name='atenciones'),
    url(r'^atenciones/(?P<pk>\d+)/$', views.atencion_single, name='atencion-single'),
    url(r'^atenciones/(?P<pk>\d+)/eliminar/$', views.atencion_eliminar, name='atencion-single-eliminar'),
    url(r'^recomendaciones/(?P<pk>\d+)/$', views.recomendacion_paciente, name='recomendacion-paciente'),
    url(r'^recomendaciones/(?P<pk>\d+)/save/$', views.recomendacion_paciente_save, name='recomendacion-paciente'),
    url(r'^recomendaciones/(?P<pk>\d+)/crear/$', views.recomendacion_paciente_crear, name='recomendacion-paciente-crear')
    ]