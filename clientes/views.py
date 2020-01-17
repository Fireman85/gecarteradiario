from django.shortcuts import render

from django.views.generic import CreateView

from .models import Cliente


from django_datatables_view.base_datatable_view import BaseDatatableView
from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.db.models import Q,F,Sum, Value as V


from django.contrib.auth.decorators import login_required



class NuevoClienteCreateView(CreateView):
    model = Cliente
    template_name = 'clientes/cliente_new.html'
    fields = '__all__'


class ClientesList110(TemplateView):
    template_name = 'clientes/cliente_new.html'


class ClientesList110Json(BaseDatatableView):
	model = Cliente
	columns = ['id','cedula', 'nombres',  'apellidos',  'telefono_celular','accion']

	def filter_queryset(self, qs):
		search = self.request.GET.get(u'search[value]', None)
		if search:
			qs = qs.filter(Q(id__istartswith=search) | Q(cedula__istartswith=search) | Q(nombres__istartswith=search) | Q(apellidos__istartswith=search))

		#print (qs)

		return qs

	def render_column(self, row, column):
		if column == 'accion':
			return mark_safe('<a href="#" >Consulta</a>') #135X140 #<a href="{0}"><img src="{0}" width="100" height="110" alt="Sin foto"></a>
		else:
			return super(ClientesList110Json, self).render_column(row, column)


	def get_initial_queryset(self):
		#id_prest = self.request.GET.get('id_prestamo', None)
		return Cliente.objects.values('id','cedula','nombres','apellidos','telefono_celular').order_by('nombres')

	def prepare_results(self, qs):
		json_data = []
		for item in qs:
			json_data.append([item["id"],item["cedula"],item["nombres"],item["apellidos"],item["telefono_celular"], mark_safe('<a href="#" class="btn btn-outline-warning btn-sm" role="button">Editar</a><a href="#" class="btn btn-outline-info btn-sm" role="button">Prestamos</a>') ])

		return json_data
