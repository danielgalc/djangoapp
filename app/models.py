from django.db import models
from django.contrib.auth.models import User


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
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank = True)

    def __str__(self):
        return self.name
    

# MODELO RENTEL INCIDENCIAS

class Cliente(models.Model):
    username = models.CharField(max_length=20, null=True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    clave = models.CharField(max_length=7)
    dni = models.CharField(max_length=9)
    tlf = models.TextField()
    direccion = models.TextField()
    email = models.EmailField(null=True)
    

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

