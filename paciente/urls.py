from django.conf.urls import url
from paciente import views


urlpatterns = [
    url(r'^$', views.inicio_paci, name='paciente'),
    url(r'^minuta/(?P<pk_paciente>\d+)/$', views.minuta_paciente, name='minuta-paciente'),
    url(r'^grupos-permitidos/(?P<pk_paciente>\d+)/$', views.grupos_permitidos, name='grupos-permitidos-paciente'),
    url(r'^evaluacion-nutricional/$', views.evaluacion_nutricional, name='evaluacion-nutricional'),
    url(r'^nutricionista/$', views.mi_nutricionista, name='mi-nutricionista'),    
]
