import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.contrib.auth.hashers import make_password
    
# MODELO RENTEL INCIDENCIAS

# MODELO PERSONALIZADO USUARIO Y SUPERUSUARIO(ADMIN)

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre=None, apellido=None, dni=None, tlf=None, direccion=None, rol="CLIENTE", password=None, is_staff=False, is_superuser=False,):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nombre=nombre,
            apellido=apellido,
            rol=rol,
            dni=dni,
            tlf=tlf,
            direccion=direccion,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', "ADMIN")

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password=password, **extra_fields)



class Usuario(AbstractBaseUser, PermissionsMixin):
    user = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
    #username = models.CharField(max_length=20, default=None)
    email = models.EmailField(
                    verbose_name='email address',
                    max_length=255,
                    unique=True,
                )
    password = models.CharField(max_length=20, default=None)
    nombre = models.CharField(max_length=20, null=True)
    apellido = models.CharField(max_length=20, null=True)
    dni = models.CharField(max_length=9, null=True)

    ROL_CHOICES = (("CLIENTE", "Cliente"),
                   ("SOPORTE", "Soporte"),
                   ("TECNICO", "Tecnico"),
                   ("ADMIN", "Admin"),)
    
    rol = models.CharField(max_length=7, choices=ROL_CHOICES)
    tlf = models.CharField(max_length=9, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['nombre', 'apellido', 'tlf', 'dni', 'direccion']

    objects = UsuarioManager()

    #def save(self, *args, **kwargs):
    #    if not self.password:
    #        self.password = make_password('XlgHPCxL99')
    #    super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if not self.password:
            password_length = 10 # Longitud de la contraseña
            characters = string.ascii_letters + string.digits
            # Selecciona caracteres al azar de la cadena de caracteres definida
            password = ''.join(random.choice(characters) for _ in range(password_length))
            self.password = make_password(password)
            print(password)
        super().save(*args, **kwargs)

# MODELO INCIDENCIA. [Zona Cliente]

class Incidencia(models.Model):
    titulo_incidencia = models.CharField(max_length=255, null=True)
    desc_incidencia = models.TextField()
    fecha = models.DateTimeField(null=True, editable=True)
    asignada = models.BooleanField(default=False)
    direccion = models.CharField(max_length=255, null=True)
    cliente_id = models.ForeignKey(
        Usuario,
        related_name="incidencias",
        on_delete=models.CASCADE
   )

