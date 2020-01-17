from django.contrib import admin

from .models import (Interes, TiposPrestamo, Descuento, Prestamo, Abono, EstadoAbono, 
UnionCuentas, PlanFinanciero, PlanFinancieroDetalle, UnionCuentasDetalle, EstadoPrestamo)



class PrestamoAdmin(admin.ModelAdmin):
    exclude = ('valor_interes', 'saldo_capital', 'saldo_interes', 'fecha_registro','estado','prestamo_nuevo',)

class PlanFinancieroDetalleInline(admin.TabularInline):
    model = PlanFinancieroDetalle

class PlanFinancieroAdmin(admin.ModelAdmin):
    inlines = [
        PlanFinancieroDetalleInline,
    ]



admin.site.register(Interes)
admin.site.register(TiposPrestamo)
admin.site.register(Descuento)
admin.site.register(Prestamo,PrestamoAdmin)
admin.site.register(EstadoAbono)
admin.site.register(EstadoPrestamo)
admin.site.register(Abono)
admin.site.register(UnionCuentas)
admin.site.register(UnionCuentasDetalle)
admin.site.register(PlanFinanciero,PlanFinancieroAdmin)
admin.site.register(PlanFinancieroDetalle)

