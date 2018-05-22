from django.db import models
import datetime
# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)


# Create your models here.

#LOS SIGUIENTES METODOS ESTAN ESCRITOS EN INGLES PORQUE SOBREESCRIBEN FUNCIONALIDAD DE LA CLASE QUEHEREDAN
class UserManager(BaseUserManager):
    def create(self, email, password):
        if not email:
            raise ValueError('Debes ingresar un email correcto.')
        if not rut:
            raise ValueError('Debes ingresar un rut') 
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superadmin(self, email, password):
        user = self.create(email, password)

        user.es_superadmin = True
        user.save(using=self._db)
        return user

    def create_user(self, rut, email, es_paciente, es_nutri, password=None):

        if not email:
            raise ValueError('Debes ingresar un email correcto.')
        if not rut:
            raise ValueError('Debes ingresar un rut') 

        user = self.model(
            rut=rut,
            email=self.normalize_email(email),
            es_paciente = es_paciente,
            es_nutri = es_nutri
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Crea y guarda un usuario staff con email, contraseña.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, rut, es_paciente, es_nutri, password):
        """
        Crea y guarda un superusuario con email y contraseña
        """
        user = self.create_user(
            email = email,
            rut = rut,
            password=password,
            es_paciente = es_paciente,
            es_nutri = es_nutri
        )
        user.staff = True
        user.admin = True
        user.rut = rut
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    #Información personal - obligatiorios
    rut = models.CharField(max_length=12)
    email = models.EmailField(
        verbose_name = 'correo electrónico',
        max_length=100,
        unique=True
    )
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    nacimiento = models.DateField(null=True, blank=True)

    M = 'M'
    F = 'F'
    GENEROS = (
        (M, 'Masculino'),
        (F, 'Femenino')
    )
    genero = models.CharField(max_length=2, choices=GENEROS, default=F)

    #Permisos y accesos
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    es_nutri = models.BooleanField(default=False)
    es_paciente = models.BooleanField(default=False)
    es_superadmin = models.BooleanField(default=False)
    USERNAME_FIELD = ('email')
    REQUIRED_FIELDS = ['rut','es_paciente','es_nutri'] #'rut','nombres','apellidos','nacimiento'
    
    #PROPIEDADES
    @property
    def is_staff(self):
        "¿Es el usuario staff?"
        return self.staff

    @property
    def is_admin(self):
        "¿Es el usuario administrador?"
        return self.admin

    @property
    def is_active(self):
        "Esta el usuario activo?"
        return self.active

    @property
    def is_nutri(self):
        "¿Es el usuario nutricionista?"
        return self.es_nutri
    
    @property
    def is_paci(self):
        "¿Es el usuario paciente?"
        return self.es_paciente
    
    def has_perm(self, perm, obj=None):
        """
        Tiene permisos ?
        """
        return True

    def has_module_perms(self, app_label):
        """
        Aca vamos a restringir accesos a ciertos modulos
        """
       
        return True

    def get_nombre(self):
        """
        Devuelve un string email
        """
        return self.email

    @property
    def get_nombre_completo(self):
        """
        Devuelve nombre y apellidos
        """
        return "{nombres} {apellidos}".format(nombres=self.nombres, apellidos=self.apellidos) if self.nombres + self.apellidos != "" else self.rut
    
    def __str__(self):
        """
        Al imprimir el objeto
        """
        string = "{} - {}".format(self.rut, self.email) 
        return string

    
    objects = UserManager()