from django.db import models
from clientes.models import Cliente
#from django.contrib.auth.models import User

#from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
#from users.models import Cobrador


class Interes(models.Model):
	porcentaje = models.FloatField()
	descripcion = models.TextField(max_length=140)

	def __str__(self):
		return str(self.porcentaje)

class TiposPrestamo(models.Model):
	tipo = models.CharField(max_length=30)

	def __str__(self):
		return self.tipo



class EstadoAbono(models.Model):
	estado = models.CharField(max_length=30)

	def __str__(self):
		return self.estado

class EstadoPrestamo(models.Model):
	estado = models.CharField(max_length=40)

	def __str__(self):
		return self.estado

		
class Prestamo(models.Model):
	
    
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
	fecha_prestamo = models.DateField(default=timezone.now)
	capital_prestado = models.FloatField()
	meses_plazo = models.IntegerField(verbose_name='Tiempo plazo')
	porcentaje_aplicado = models.ForeignKey(Interes, on_delete=models.CASCADE)
	valor_interes = models.FloatField(null=True)
	saldo_capital = models.FloatField(null=True)
	saldo_interes = models.FloatField(null=True)
	tipo_prestamo = models.ForeignKey(TiposPrestamo, on_delete=models.CASCADE)
	fecha_registro = models.DateTimeField(default=timezone.now)
	prestamo_nuevo = models.ForeignKey('Prestamo', on_delete=models.CASCADE, blank= True, null=True)
	estado = models.ForeignKey('EstadoPrestamo', on_delete = models.CASCADE, blank= True, default=1)
	#estado = models.IntegerField(choices=ESTADOS, default=PENDIENTE, blank= True)
	observaciones = models.TextField(max_length=150,blank=True)
	cobrador = models.ForeignKey(get_user_model(), on_delete= models.CASCADE, default='')

	def __str__(self):
		return "{0},{1},{2}".format(self.fecha_prestamo, self.cliente, self.capital_prestado)

class Abono(models.Model):
	prestamo = models.ForeignKey(Prestamo,on_delete=models.CASCADE)
	fecha_abono = models.DateField(default=timezone.now)
	valor_abono_capital = models.FloatField()
	valor_abono_interes = models.FloatField()
	observaciones = models.TextField(max_length=100,blank=True,null=True)
	fecha_registro = models.DateTimeField(default=timezone.now)
	estado = models.ForeignKey(EstadoAbono, on_delete = models.CASCADE, blank= True, null=True)
	cobrador = models.ForeignKey(get_user_model(), on_delete= models.CASCADE, default='')

	def __str__(self):
		return "{0},{1}".format(self.fecha_abono, self.valor_abono_capital)


class Descuento(models.Model):
	prestamo = models.ForeignKey(Prestamo,on_delete=models.CASCADE)
	fecha_descuento = models.DateField(default=timezone.now)
	valor_descuento = models.FloatField(default=0, null=False)
	fecha_registro = models.DateTimeField(default=timezone.now)
	descontadopor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	
	def __str__(self):
		return "descuento: {0}, {1}".format(self.fecha_descuento, self.valor_descuento)

class UnionCuentas(models.Model):
	fecha_union = models.DateField(default=timezone.now)
	fecha_registro = models.DateTimeField(default=timezone.now)
	capital_total = models.FloatField()
	valor_abono_capital_total = models.FloatField()
	valor_abono_interes_total = models.FloatField()
	saldo = models.FloatField() #este saldo es saldo al capital
	#usuario = models.ForeignKey(User, on_delete= models.CASCADE)

	def __str__(self):
		return "{},{}".format(self.fecha_union,self.saldo)
	
class UnionCuentasDetalle(models.Model):
	union_cuentas = models.ForeignKey(UnionCuentas, on_delete=models.CASCADE)
	prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE)
	

	def __str__(self):
		return "detalle id: {0}, maestro id: {1}, prestamo id: {2}".format(self.id, self.union_cuentas, self.prestamo.id)

class PlanFinanciero(models.Model):
	fecha_registro = models.DateTimeField(default=timezone.now)
	#usuario = models.ForeignKey(User, on_delete= models.CASCADE)
	cliente = models.ForeignKey(Cliente, on_delete= models.CASCADE)
	prestamo = models.ForeignKey(Prestamo, on_delete= models.CASCADE)

	def __str__(self):
		return "{}-{}-{}".format(self.usuario, self.cliente, self.prestamo)

class PlanFinancieroDetalle(models.Model):
	plan_financiero = models.ForeignKey(PlanFinanciero, on_delete= models.CASCADE)
	fecha_abono = models.DateField(default=timezone.now)
	valor_capital = models.FloatField()
	valor_interes = models.FloatField()
	concepto = models.CharField(max_length=80)

	def __str__(self):
		return "{}-{}-{}-{}".format(self.plan_financiero, self.valor_capital, self.valor_interes, self.concepto)






