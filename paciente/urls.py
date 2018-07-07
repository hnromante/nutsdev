from django.conf.urls import url
from paciente import views


urlpatterns = [
    url(r'^$', views.inicio_paci, name='paciente'),
    url(r'^minuta/(?P<pk_paciente>\d+)/$', views.minuta_paciente, name='minuta-paciente'),    
]
