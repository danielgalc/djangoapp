from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model



class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)

    def __str__(self):
        return self.name
    
class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    #venue = models.CharField(max_length=120)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank = True)

    def __str__(self):
        return self.name
    
# MODELO RENTEL INCIDENCIAS




# MODELO ADMIN


class ClienteManager(BaseUserManager):
    def create_user(self, email, password=None, rol=None, is_staff=False, is_superuser=False,):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

        user.set_password(password)
        user.save(using=self._db)

        user.rol = rol
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

        return self.create_user(email, password, **extra_fields)



class Cliente(AbstractBaseUser, PermissionsMixin):
    user = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True, default=None)
    #username = models.CharField(max_length=20, default=None)
    email = models.EmailField(
                    verbose_name='email address',
                    max_length=255,
                    unique=True,
                )
    password = models.CharField(max_length=20, default=None)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    dni = models.CharField(max_length=9)

    ROL_CHOICES = (("CLIENTE", "Cliente"),
                   ("SOPORTE", "Soporte"),
                   ("TECNICO", "Tecnico"),
                   ("ADMIN", "Admin"),)
    
    rol = models.CharField(max_length=7, choices=ROL_CHOICES)
    tlf = models.CharField(max_length=9)
    direccion = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['rol']

    objects = ClienteManager()
    
    def crear_cliente(sender, instance, created, **kwargs):
        if created:
            profile, created = Cliente.objects.get_or_create(user=instance)

    post_save.connect(crear_cliente, sender=User)
















class Incidencia(models.Model):
    titulo_incidencia = models.CharField(max_length=255, null=True)
    desc_incidencia = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    asignada = models.BooleanField(default=False)
    direccion = models.CharField(max_length=255, null=True)
    cliente_id = models.ForeignKey(
        Cliente,
        related_name="incidencias",
        on_delete=models.CASCADE
    )

