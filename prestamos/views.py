from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#from django.contrib.auth.models import User
import json

from .forms import PrestamoForm, AbonoForm, DescuentoForm
from clientes.models import Cliente
from .models import ( Prestamo,TiposPrestamo,Interes,Abono,EstadoAbono,
	PlanFinanciero, PlanFinancieroDetalle,UnionCuentas,UnionCuentasDetalle, Descuento
	)

from django.contrib.auth import get_user_model

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.db.models import Q,F,Sum, Value as V, OuterRef, Subquery, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce
from django.utils.html import escape

import datetime
from datetime import timedelta
from django.utils import timezone

import calendar #realmente usando

from django.contrib.auth.decorators import login_required

@login_required
def nuevo_union_cuentas(request):
	if request.method=='GET':
		form = PrestamoForm()
		return render(request,'prestamos/unioncuentas.html',{'form': form})
	else:
		form = PrestamoForm(request.POST)

		if form.is_valid():
			prestamo_object = Prestamo()
			
			form.save(commit=False)
			id_client = request.POST['id_cliente']
			id_prestamus = request.POST['id_prestamo']
			#print (id_client)
			form.cliente = Cliente.objects.get(id=id_client)
			prestamo_obj_viejo = Prestamo.objects.get(id=id_prestamus)
			
			prestamo_object.cliente= Cliente.objects.get(id=id_client)
			cobradore = get_user_model()
			prestamo_object.cobrador= cobradore#request.user
			prestamo_object.fecha_prestamo = request.POST['fecha_prestamo']
			prestamo_object.capital_prestado = float(request.POST['capital_prestado'])
			prestamo_object.tipo_prestamo = TiposPrestamo.objects.get(id=request.POST['tipo_prestamo'])
			prestamo_object.meses_plazo = int(request.POST['meses_plazo'])
			prestamo_object.porcentaje_aplicado = Interes.objects.get(id=request.POST['porcentaje_aplicado'])
			prestamo_object.observaciones = request.POST['observaciones']
			prestamo_object.prestamo_nuevo = Prestamo.objects.get(id=id_prestamus)
			prestamo_object.estado = 3 #fusionado
						
			prestamo_object.save()

			form.usuario = cobradore#request.user

			#guardar union cuentas maestro y detalle
			unionc = UnionCuentas()
			unionc.capital_total = prestamo_object.capital_prestado + prestamo_obj_viejo.capital_prestado
			Tabono_a_capital = Abono.objects.filter(prestamo=prestamo_object.id).aggregate(tot_valo_abo=Coalesce(Sum('valor_abono_capital'), V(0))).get('tot_valo_abo') #Abono.objects.filter(prestamo=prestamo_object.id).aggregate(tota_abono_capital=Coalesce(Sum('valor_abono_capital'), V(0))).get('tota_abono_capital')
			Tabono_a_capital_2 = Abono.objects.filter(prestamo=prestamo_obj_viejo.id).aggregate(tot_valo_abo_e=Coalesce(Sum('valor_abono_capital'), V(0))).get('tot_valo_abo_e')#Abono.objects.filter(prestamo=prestamo_obj_viejo.id).aggregate(tota_abono_interes=Coalesce(Sum('valor_abono_capital'), V(0)).get('tota_abono_interes'))

			#print ('Tabono_a_capital: {}'.format(Tabono_a_capital))
			#print ('Tabono_interes: {}'.format(Tabono_a_capital_2))

			unionc.valor_abono_capital_total = Tabono_a_capital + Tabono_a_capital_2
			unionc.valor_abono_interes_total = Abono.objects.filter(prestamo=prestamo_object.id).aggregate(tot_valo_abo=Coalesce(Sum('valor_abono_interes'), V(0))).get('tot_valo_abo')  + Abono.objects.filter(prestamo=prestamo_obj_viejo.id).aggregate(tot_valo_abo_e=Coalesce(Sum('valor_abono_interes'), V(0))).get('tot_valo_abo_e')#float(Abono.objects.filter(prestamo=prestamo_object.id).aggregate(Coalesce(Sum('valor_abono_interes'), V(0)).get('valor_abono_interes__sum'))) + float(Abono.objects.filter(prestamo=prestamo_obj_viejo.id).aggregate(Coalesce(Sum('valor_abono_interes'), V(0)).get('valor_abono_interes__sum')))
			unionc.saldo = unionc.capital_total - unionc.valor_abono_capital_total
			#unionc.usuario = User.objects.first()

			unionc.save()

			unionc_detalle_1 = UnionCuentasDetalle()
			unionc_detalle_1.union_cuentas = unionc
			unionc_detalle_1.prestamo = prestamo_object
			unionc_detalle_1.save()

			unionc_detalle_2 = UnionCuentasDetalle()
			unionc_detalle_2.union_cuentas = unionc
			unionc_detalle_2.prestamo = prestamo_obj_viejo
			unionc_detalle_2.save()


			#form.save()
			#print ("en el post de creacion de union cuentas VALID")

			data = 'fail'

			data = {
    		'id': unionc.id,
    		
    		}

			return JsonResponse(data, safe=False)


			#form.cliente = 
			#form = PrestamoForm()
			#return render(request,'prestamos/unioncuentas.html',{'form': form})
		else:

			return render(request,'prestamos/unioncuentas.html',{'form': form})

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d,month=m, year=y)





class UsersList110(TemplateView):
    template_name = 'prestamos/abonosnew.html'


class AbonosList110Json(BaseDatatableView):
	model = Abono
	columns = ['id','fecha_abono', 'valor_abono_capital',  'valor_abono_interes','accion']

	def filter_queryset(self, qs):
		search = self.request.GET.get(u'search[value]', None)
		if search:
			qs = qs.filter(Q(id__istartswith=search) | Q(fecha_abono__istartswith=search) | Q(valor_abono_capital__istartswith=search))

		#print (qs)

		return qs

	def render_column(self, row, column):
		if column == 'accion':
			return mark_safe('<a href="#" >Consulta</a>') #135X140 #<a href="{0}"><img src="{0}" width="100" height="110" alt="Sin foto"></a>
		else:
			return super(AbonosList110Json, self).render_column(row, column)


	def get_initial_queryset(self):
		id_prest = self.request.GET.get('id_prestamo', None)
		return Abono.objects.values('id','fecha_abono','valor_abono_capital','valor_abono_interes').filter(prestamo__id=id_prest).order_by('fecha_abono')

	def prepare_results(self, qs):
		json_data = []
		for item in qs:
			json_data.append([item["id"],item["fecha_abono"].strftime("%d-%m-%Y"),escape('{:,}'.format(item["valor_abono_capital"])),escape('{:,}'.format(item["valor_abono_interes"])), mark_safe('<a href="#" class="btn btn-outline-warning btn-sm" role="button">Editar</a><button type="submit" onclick="borrarAbono(this);" class="btn btn-outline-danger btn-sm">Borrar</button>') ])

		return json_data


class DescuentosList110Json(BaseDatatableView):
	model = Descuento
	columns = ['id','fecha_descuento', 'valor_descuento','accion']

	def filter_queryset(self, qs):
		search = self.request.GET.get(u'search[value]', None)
		if search:
			qs = qs.filter(Q(id__istartswith=search) | Q(fecha_descuento__istartswith=search) | Q(valor_descuento__istartswith=search))

		#print (qs)

		return qs

	def render_column(self, row, column):
		if column == 'accion':
			return mark_safe('<a href="#" >Consulta</a>') #135X140 #<a href="{0}"><img src="{0}" width="100" height="110" alt="Sin foto"></a>
		else:
			return super(DescuentosList110Json, self).render_column(row, column)


	def get_initial_queryset(self):
		id_prest = self.request.GET.get('id_prestamo', None)
		return Descuento.objects.values('id','fecha_descuento','valor_descuento').filter(prestamo__id=id_prest).order_by('fecha_descuento')

	def prepare_results(self, qs):
		json_data = []
		for item in qs:
			json_data.append([item["id"],item["fecha_descuento"].strftime("%d-%m-%Y"),escape('{:,}'.format(item["valor_descuento"])), mark_safe('<a href="#" class="btn btn-outline-warning btn-sm" role="button">Editar</a><button type="submit" onclick="borrarDescuento(this);" class="btn btn-outline-danger btn-sm">Borrar</button>') ])

		return json_data


class PrestamosTodosList110Json(BaseDatatableView):
	model = Prestamo
	columns = ['id','fecha_prestamo', 'cliente', 'cliente',  'capital_prestado','tipo_prestamo','accion']
	#order_columns = ['capital_prestado']

	#def render_column(self, row, column):
		#if column == 'accion':
			#return mark_safe('<a href="#" >Consulta</a>') #135X140 #<a href="{0}"><img src="{0}" width="100" height="110" alt="Sin foto"></a>
		#else:
			#return super(UsersList110Json, self).render_column(row, column)

	def filter_queryset(self, qs):
		search = self.request.GET.get(u'search[value]', None)
		if search:
			qs = qs.filter(Q(id__istartswith=search) | Q(fecha_prestamo__istartswith=search) | Q(capital_prestado__istartswith=search) | Q(cliente__nombres__istartswith=search) | Q(cliente__apellidos__istartswith=search))

		#print (qs)

		return qs

	def get_initial_queryset(self):
		return Prestamo.objects.values('id','fecha_prestamo','cliente__nombres','cliente__apellidos','capital_prestado','tipo_prestamo__tipo').filter(estado=1).order_by('-fecha_prestamo')

	def prepare_results(self, qs):
		json_data = []
		for item in qs:
			json_data.append([item["id"],item["fecha_prestamo"].strftime("%d-%m-%Y"),item["cliente__nombres"],item["cliente__apellidos"],escape('{:,}'.format(item["capital_prestado"])),item["tipo_prestamo__tipo"], mark_safe('<button id = "btEditarPrestamo"  type="submit" class="btn btn-outline-warning btn-sm">Editar</button><button type="submit" onclick="borrarPrestamo(this);" class="btn btn-outline-danger btn-sm">Borrar</button>') ])

		return json_data



class PrestamosList110Json(BaseDatatableView):
	
	#model = Prestamo
	columns = ['id','capital_prestado', 'fecha_prestamo',  'porcentaje_aplicado__porcentaje','abonos_capital','saldo_capital','accion']
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

		#print (qs)

		return qs

	def get_initial_queryset(self):
		id_cli = self.request.GET.get('id_cliente', None)
		#print ("id_cli: {0}".format(id_cli))
		descuentos_prestam = Descuento.objects.filter(prestamo=OuterRef('pk')).values('prestamo').annotate(descuento_prestamo=Coalesce(Sum('valor_descuento'),V(0))).values('descuento_prestamo')

		return Prestamo.objects.values('id','capital_prestado','fecha_prestamo','porcentaje_aplicado__porcentaje').annotate(abonos_capital=Coalesce(Sum('abono__valor_abono_capital'),V(0)),abonos_interes=Coalesce(Sum('abono__valor_abono_interes'),V(0)),saldo_capital=ExpressionWrapper(F('capital_prestado')- Coalesce(Sum('abono__valor_abono_capital'),V(0)) - Coalesce( Subquery(descuentos_prestam.values('descuento_prestamo')) , 0), output_field=FloatField()),saldo_interes=F('saldo_capital') * F('porcentaje_aplicado__porcentaje')/100.0 ).filter(cliente__id=id_cli,estado=1).order_by('-fecha_prestamo')

	def prepare_results(self, qs):
		json_data = []
		for item in qs:
			json_data.append([item["id"],escape('{:,}'.format(item["capital_prestado"])),item["fecha_prestamo"].strftime("%d-%m-%Y"), escape('{0} %'.format(item["porcentaje_aplicado__porcentaje"])),escape('{:,}'.format(item["abonos_capital"])),escape('{:,}'.format(item["saldo_capital"])), mark_safe('<a href="#" class="btn btn-outline-warning btn-sm" role="button">Editar</a><button type="submit" onclick="consultaEstadoCuenta(this);" class="btn btn-outline-info btn-sm">Cuenta</button>') ])

		return json_data

        

def mostrar_estado_cuenta(request):
	id_prestam = request.GET.get('id_prestamo', None)
	return render(request,'prestamos/estado_cuenta.html', {'id_prestam': id_prestam})


class UsersList110Json(BaseDatatableView):
	
	#model = Prestamo
	columns = ['id','capital_prestado', 'fecha_prestamo',  'porcentaje_aplicado__porcentaje','abonos_capital','saldo_capital','accion']
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

		#print (qs)

		return qs

	def get_initial_queryset(self):
		return Prestamo.objects.values('id','capital_prestado','fecha_prestamo','porcentaje_aplicado__porcentaje').annotate(abonos_capital=Coalesce(Sum('abono__valor_abono_capital'),V(0)),abonos_interes=Coalesce(Sum('abono__valor_abono_interes'),V(0)),saldo_capital=F('capital_prestado')- Coalesce(Sum('abono__valor_abono_capital'),V(0)),saldo_interes=F('saldo_capital') * F('porcentaje_aplicado__porcentaje')/100.0 ).filter(cliente__id=1,estado__id=1).order_by('-fecha_prestamo')

	def prepare_results(self, qs):
		json_data = []
		for item in qs:
			json_data.append([item["id"],escape('{:,}'.format(item["capital_prestado"])),item["fecha_prestamo"].strftime("%d-%m-%Y"), escape('{0} %'.format(item["porcentaje_aplicado__porcentaje"])),escape('{:,}'.format(item["abonos_capital"])),escape('{:,}'.format(item["saldo_capital"])), mark_safe('<a href="#" >Borrar</a>') ])

		return json_data

        


		#return Prestamo.objects.all()

        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        
    #esto estaba afuera debajo del nombre de la clase
    #model = Prestamo
    #columns = ['id','fecha_prestamo', 'capital_prestado', 'porcentaje_aplicado', 'tipo_prestamo','accion']
    
    
@login_required
def home(request):
	return render(request,'prestamos/index.html')

def borrar_Prestamo(request):
	if request.method == 'POST':
		id_prestamo = request.POST['id_prestamo']
		detalle_respuesta = ''

		cant_abonos_del_prestamo = Abono.objects.filter(prestamo=id_prestamo).count()

		if cant_abonos_del_prestamo > 0 :
			detalle_respuesta = ' Anulado.'
			prestam_object = Prestamo.objects.get(id=id_prestamo)
			prestam_object.estado = 4
			prestam_object.save()
			
		else:
			detalle_respuesta = ' Eliminado.'
			prestam_object = Prestamo.objects.get(id=id_prestamo)
			prestam_object.delete()

				
		data = {
			'detalle_respuesta': detalle_respuesta
			
			}
		return JsonResponse(data)
	else:
		form = PrestamoForm()
		return render(request,'prestamos/prestamosnew.html',{'form': form})


def borrar_Abono(request):
	if request.method == 'POST':
		id_abono = request.POST['id_abono']
		detalle_respuesta = ''

		prestamo_dic = Abono.objects.values('prestamo').get(id = id_abono)
		cliente_dic = Abono.objects.values('prestamo__cliente').get(id = id_abono)

		abono_object = Abono.objects.get(id=id_abono)
		abono_object.delete()

				
		data = {
			'detalle_respuesta': 'ok',
			'id_prestam': prestamo_dic.get('prestamo'),
			'id_client': cliente_dic.get('prestamo__cliente')
			
			
			}
		return JsonResponse(data)
	else:
		form = AbonoForm()
		return render(request,'prestamos/abonosnew.html',{'form': form})

def borrar_Descuento(request):
	if request.method == 'POST':
		id_descuento = request.POST['id_descuento']
		detalle_respuesta = ''

		prestamo_dic = Descuento.objects.values('prestamo').get(id = id_descuento)
		cliente_dic = Descuento.objects.values('prestamo__cliente').get(id = id_descuento)

		descuento_object = Descuento.objects.get(id=id_descuento)
		descuento_object.delete()

				
		data = {
			'detalle_respuesta': 'ok',
			'id_prestam': prestamo_dic.get('prestamo'),
			'id_client': cliente_dic.get('prestamo__cliente')
			
			
			}
		return JsonResponse(data)
	else:
		form = DescuentoForm()
		return render(request,'prestamos/descuentos.html',{'form': form})


@login_required
def nuevo_Abono(request):
	if request.method=='GET':
		form = AbonoForm()
		return render(request,'prestamos/abonosnew.html',{'form': form})
	else:
		form = AbonoForm(request.POST)

		if form.is_valid():
			abono_object = Abono()
			
			form.save(commit=False)
			id_prestamo = request.POST['id_prestamo']
			#print ("El id del prestamo es: {}".format(id_prestamo))
			form.prestamo = Prestamo.objects.get(id=id_prestamo)
			abono_object.fecha_abono= request.POST['fecha_abono']
			abono_object.valor_abono_capital = request.POST['valor_abono_capital']
			abono_object.valor_abono_interes = request.POST['valor_abono_interes']
			abono_object.observaciones = request.POST['observaciones']
			abono_object.fecha_registro = datetime.datetime.now()
			abono_object.estado = 1
			cobradore = get_user_model()
			abono_object.cobrador = cobradore#User.objects.first()
			
			
			abono_object.save()


			#form.usuario = User.objects.first()

			
			#print ("en el post de creacion de abono VALID")
			#form = PrestamoForm()
			#return render(request,'prestamos/abonosnew.html',{'form': form})
		else:

			return render(request,'prestamos/abonosnew.html',{'form': form})

@login_required
def descuento_Prestamo(request):
	if request.method=='GET':
		form = DescuentoForm()
		return render(request,'prestamos/descuentos.html',{'form': form})
	else:
		form = DescuentoForm(request.POST)

		if form.is_valid():
			descuento_object = Descuento()
			
			form.save(commit=False)
			id_prestamo = request.POST['id_prestamo']
			form.prestamo = Prestamo.objects.get(id=id_prestamo)
			
			descuento_object.valor_descuento = request.POST['valor_descuento']
			descuento_object.fecha_descuento = datetime.datetime.now()
			cobradore = get_user_model()
			descuento_object.descontadopor = cobradore.username#request.user.username #User.objects.first()
			
			
			descuento_object.save()


			#form.usuario = User.objects.first()

			
			#print ("en el post de creacion de abono VALID")
			#form = PrestamoForm()
			#return render(request,'prestamos/abonosnew.html',{'form': form})
		else:

			return render(request,'prestamos/descuentos.html',{'form': form})

@login_required
def nuevo_Prestamo(request):
	if request.method=='GET':
		form = PrestamoForm()
		return render(request,'prestamos/prestamosnew.html',{'form': form})
	else:
		form = PrestamoForm(request.POST)
		#print ("antes de validar el form")

		if form.is_valid():
			#print ("dentro de validation form")
			prestamo_object = Prestamo()
				
			form.save(commit=False)
			id_client = request.POST['cliid']
			#print (id_client)
			client_object = Cliente.objects.get(id=id_client) 
			form.cliente = client_object
				
			prestamo_object.cliente= Cliente.objects.get(id=id_client)
			cobradore = get_user_model().objects.all()[0]
			cobradore = get_user_model().objects.get(username=request.user)
			print(cobradore)
			
			prestamo_object.cobrador= cobradore#User.objects.first()
			prestamo_object.fecha_prestamo = request.POST['fecha_prestamo']
			prestamo_object.capital_prestado = request.POST['capital_prestado']
			prestamo_object.tipo_prestamo = TiposPrestamo.objects.get(id=request.POST['tipo_prestamo'])
			prestamo_object.meses_plazo = int(request.POST['meses_plazo'])
			prestamo_object.porcentaje_aplicado = Interes.objects.get(id=request.POST['porcentaje_aplicado'])
			prestamo_object.observaciones = request.POST['observaciones']
			#state = EstadoPrestamo.objects.all()[0]
			#prestamo_object.estado = state
				
				
			prestamo_object.save()

			#crea plan financiero automaticamente para luego guardarlos junto al detalle
			pf = PlanFinanciero()
			#pf.usuario = cobradore#User.objects.first()
			pf.cliente = client_object
			pf.prestamo = prestamo_object
			pf.save()

			valor_cuota = float(prestamo_object.capital_prestado)/float(prestamo_object.meses_plazo)
			saldo = float(prestamo_object.capital_prestado)
			fecha_inicio = prestamo_object.fecha_prestamo
			suma_mes = 1

			#agrega los detalles del plan financiero

			for i in range(int(prestamo_object.meses_plazo)):
				pf_detalle = PlanFinancieroDetalle()
				pf_detalle.plan_financiero = pf
				pf_detalle.fecha_abono= monthdelta(datetime.datetime.strptime(str(fecha_inicio), "%Y-%m-%d").date(), suma_mes) #pagar el primer dia de cada mes
				
				pf_detalle.valor_capital=valor_cuota
				pf_detalle.valor_interes=(saldo)*(float(prestamo_object.porcentaje_aplicado.porcentaje)/100.0)

				saldo = saldo - valor_cuota
				#fecha_inicio = pf_detalle.fecha_abono
				suma_mes = suma_mes + 1

				
				pf_detalle.concepto="Cuota {}".format(i+1)
				pf_detalle.save()


			#form.cobrador = cobradore#User.objects.first()



				#form.save()
			#print ("en el post de creacion de prestamo VALID")
				#form.cliente = 
			form = PrestamoForm()
			data = {
				'id_prestamo': prestamo_object.id,
				'id_cliente': prestamo_object.cliente.id #id del cliente
			}
			#print(data)
			return JsonResponse(data)

			#return render(request,'prestamos/prestamosnew.html',{'form': form})
		else:
			#print("form no validate")
			#print(form.errors)

			return render(request,'prestamos/prestamosnew.html',{'form': form})

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '')#.capitalize()
        q = q.strip()
        results = []
        search_qs = Cliente.objects.filter(nombres__startswith=q) | Cliente.objects.filter(apellidos__startswith=q)
        
        # (q)
        for r in search_qs:
            results.append("{},{}".format(r.nombres, r.apellidos))
            #print (r.nombres)
        #if len(results)==0:
        	#search_qs = Cliente.objects.filter(apellidos__startswith=q)
        	#for r in search_qs:
        		#results.append("{} {}".format(r.apellidos, r.nombres))
        		#print (r.nombres)


        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def traerDatosdeCliente(request):
    cliNom = request.GET.get('nombres', None)
    cliApp = request.GET.get('apellidos', None)

    data='fail'

    if cliNom!='' or cliApp!='':
    	nom = cliNom.strip()
    	app = cliApp.strip()

    	existe = Cliente.objects.filter(nombres__iexact=nom, apellidos__iexact=app).exists()


    	if existe:
    		cli_object = Cliente.objects.get(nombres__iexact=nom, apellidos__iexact=app)
    		data = {
    		'id': cli_object.id,
    		'nombres': cli_object.nombres,
    		'apellidos': cli_object.apellidos,
    		'direccion': cli_object.direccion,
    		'telefono_celular': cli_object.telefono_celular,
    		}
    return JsonResponse(data, safe=False)

@login_required
def registrar_abono(request):
	if request.method=='GET':
		form = AbonoForm()
		return render(request,'prestamos/abonosnew.html',{'form': form})
	else:
		form = AbonoForm(request.POST)

		#if form.is_valid():
		abono_object = Abono()
			
		form.save(commit=False)
		id_prestamo = request.POST['id_prestamo']
		#print ("El id del prestamo es: {}".format(id_prestamo))
		#form.prestamo = Prestamo.objects.get(id=id_prestamo)
		abono_object.prestamo = Prestamo.objects.get(id=id_prestamo)
		abono_object.fecha_abono = request.POST['fecha_abono']
		abono_object.valor_abono_capital = request.POST['valor_abono_capital']
		abono_object.valor_abono_interes = request.POST['valor_abono_interes']
		abono_object.observaciones = request.POST['observaciones']
		abono_object.fecha_registro = datetime.datetime.now()
		abono_object.estado = EstadoAbono.objects.all()[0]
		cobradore = get_user_model()
		abono_object.usuario = cobradore#User.objects.first()
			
			
		abono_object.save()
		data = {
			'id_abono': abono_object.id,
			'id_cliente': abono_object.prestamo.cliente.id #id del cliente
			}
		return JsonResponse(data)


@login_required
def registrar_descuento(request):
	if request.method=='GET':
		form = DescuentoForm()
		return render(request,'prestamos/descuentos.html',{'form': form})
	else:
		form = DescuentoForm(request.POST)

		#if form.is_valid():
		descuento_object = Descuento()
			
		form.save(commit=False)
		id_prestamo = request.POST['id_prestamo']
		#print ("El id del prestamo es: {}".format(id_prestamo))
		#form.prestamo = Prestamo.objects.get(id=id_prestamo)
		descuento_object.prestamo = Prestamo.objects.get(id=id_prestamo)
		descuento_object.fecha_descuento = datetime.datetime.now()
		descuento_object.valor_descuento = request.POST['valor_descuento']
		descuento_object.fecha_registro = datetime.datetime.now()
		cobradore = get_user_model()
		descuento_object.descontadopor = cobradore.user #User.objects.first()
			
			
		descuento_object.save()
		data = {
			'id_descuento': descuento_object.id,
			'id_cliente': descuento_object.prestamo.cliente.id #id del cliente
			}
		return JsonResponse(data)


			
		



   