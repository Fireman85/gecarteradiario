from django.db import models

from django.urls import reverse

class Cliente(models.Model):
	foto = models.ImageField(upload_to = 'media/clientes/', null=True, blank=True)
	cedula = models.CharField(max_length=30, null=True, blank=True)
	nombres = models.CharField(max_length=70)
	apellidos = models.CharField(max_length=70)
	direccion = models.CharField(max_length=70, null=True, blank=True)
	telefono_fijo = models.CharField(max_length=20, null=True, blank=True)
	telefono_celular = models.CharField(max_length=20, null=True, blank=True)
	contrasena_cuenta = models.CharField(max_length=15, null=True, blank=True)
	
	def __str__(self):
		return "{0}-{1}".format(self.nombres, self.apellidos)

	def get_absolute_url(self):
		return reverse('home')
