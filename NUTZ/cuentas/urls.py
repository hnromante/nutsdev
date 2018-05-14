from django.conf.urls import url
from cuentas import views


urlpatterns = [
    url(r'^soypaciente$', views.soypaciente, name='soypaciente'),
    url(r'^soynutricionista$', views.soynutricionista, name='soynutricionista'),
    url(r'^login-nutricionista/$', views.login_nutri, name='login-nutricionista'),
    url(r'^login-paciente/$', views.login_paci, name='login-paciente'),
    url(r'^registro-nutricionista/$', views.registro_nutri, name='registro-nutricionista'),
    url(r'^logout/$', views.logout, name='logout'),
]
