from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
import json

from clientes.models import Cliente
from prestamos.models import ( Prestamo,TiposPrestamo,Interes,Abono,EstadoAbono,
	PlanFinanciero, PlanFinancieroDetalle,UnionCuentas,UnionCuentasDetalle, Descuento
	)


from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.db.models import Q,F,Sum, Value as V, ExpressionWrapper, FloatField, OuterRef, Subquery, Exists
from django.db.models.functions import Coalesce
from django.utils.html import escape

from django.db.models.functions import Concat


import datetime
from datetime import timedelta
from django.utils import timezone

import calendar #realmente usando



#para importar a archivo csv
import csv


def mostrar_prestamos_activos(request):
    return render(request, 'reportes/prestamosactivos.html')

class ReportePrestamosTodos(BaseDatatableView):
	
	#model = Prestamo
	columns = ['id','cliente','capital_prestado', 'fecha_prestamo',  'porcentaje_aplicado__porcentaje','abonos_capital','saldo_capital']
	#order_columns = ['capital_prestado']

	#def render_column(self, row, column):
		#if column == 'accion':
			#return mark_safe('<a href="#" >Consulta</a>') #135X140 #<a href="{0}"><img src="{0}" width="100" height="110" alt="Sin foto"></a>
		#else:
			#return super(UsersList110Json, self).render_column(row, column)

	def filter_queryset(self, qs):
		search = self.request.GET.get(u'search[value]', None)
		if search:
			qs = qs.filter(Q(id__istartswith=search) | Q(fecha_prestamo__istartswith=search) | Q(capital_prestado__istartswith=search))

		print (qs)

		return qs

	def get_initial_queryset(self):
		#id_cli = self.request.GET.get('id_cliente', None)
		#print ("id_cli: {0}".format(id_cli))
		
		#el django orm anterior
		#return Prestamo.objects.values('id','capital_prestado','fecha_prestamo','porcentaje_aplicado__porcentaje').annotate(cliente=Concat('cliente__nombres', V(' '),'cliente__apellidos'),abonos_capital=Coalesce(Sum('abono__valor_abono_capital'),V(0)),abonos_interes=Coalesce(Sum('abono__valor_abono_interes'),V(0)),descuentos=Coalesce(Sum('descuento__valor_descuento'),V(0)),saldo_capital=F('capital_prestado')- F('abonos_capital') ,saldo_interes=F('saldo_capital') * F('porcentaje_aplicado__porcentaje')/100.0 ).filter(estado=1).order_by('fecha_prestamo')

		#el django orm nuevo
		descuentos_prestam = Descuento.objects.filter(prestamo=OuterRef('pk')).values('prestamo').annotate(descuento_prestamo=Coalesce(Sum('valor_descuento'),V(0))).values('descuento_prestamo')
		return Prestamo.objects.values('id','capital_prestado','fecha_prestamo','porcentaje_aplicado__porcentaje').annotate(cliente=Concat('cliente__nombres', V(' '),'cliente__apellidos'),abonos_capital=Coalesce(Sum('abono__valor_abono_capital'),V(0)),abonos_interes=Coalesce(Sum('abono__valor_abono_interes'),V(0)),descuentos=Coalesce(Subquery(descuentos_prestam.values('descuento_prestamo')) ,0),saldo_capital=ExpressionWrapper(F('capital_prestado')- F('abonos_capital') - F('descuentos'),output_field=FloatField())  ,saldo_interes=F('saldo_capital') * F('porcentaje_aplicado__porcentaje')/100.0 ).filter(estado=1).order_by('fecha_prestamo')


	def prepare_results(self, qs):
		json_data = []
		for item in qs:
			json_data.append([item["id"],escape('{:,}'.format(item["capital_prestado"])),item["fecha_prestamo"].strftime("%d-%m-%Y"), escape('{0} %'.format(item["porcentaje_aplicado__porcentaje"])),item["cliente"],escape('{:,}'.format(item["abonos_capital"])),escape('{:,}'.format(item["descuentos"])),escape('{:,}'.format(item["saldo_capital"])) ])

		return json_data


def export_prestamos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cartera.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'Capital prestado', 'Fecha prestamo', 'Porcentaje', 'Cliente', 'Abonos a capital', 'Descuentos', 'Saldo a capital'])
    descuentos_prestam = Descuento.objects.filter(prestamo=OuterRef('pk')).values('prestamo').annotate(descuento_prestamo=Coalesce(Sum('valor_descuento'),V(0))).values('descuento_prestamo')
    prestamos = Prestamo.objects.values('id','capital_prestado','fecha_prestamo','porcentaje_aplicado__porcentaje').annotate(cliente=Concat('cliente__nombres', V(' '),'cliente__apellidos'),abonos_capital=Coalesce(Sum('abono__valor_abono_capital'),V(0)),abonos_interes=Coalesce(Sum('abono__valor_abono_interes'),V(0)),descuentos=Subquery(descuentos_prestam.values('descuento_prestamo')),saldo_capital=ExpressionWrapper(F('capital_prestado')- F('abonos_capital') - F('descuentos'),output_field=FloatField())  ,saldo_interes=F('saldo_capital') * F('porcentaje_aplicado__porcentaje')/100.0 ).filter(estado=1).order_by('fecha_prestamo').values_list('id', 'capital_prestado', 'fecha_prestamo', 'porcentaje_aplicado__porcentaje','cliente','abonos_capital','descuentos','saldo_capital')

    for prestamo in prestamos:
	    writer.writerow(prestamo)

    return response

