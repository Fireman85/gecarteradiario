
from django.urls import path
from .views import mostrar_prestamos_activos, ReportePrestamosTodos, export_prestamos_csv

urlpatterns = [
   path('reportes/prestamosactivos', mostrar_prestamos_activos, name='r_prestamoactivos'),
   path('reportes/prestamos/todos', ReportePrestamosTodos.as_view(), name="r_todoslosprestamos"),#ajax
   path('export/csv', export_prestamos_csv, name='export_prestamos_csv_list'),
  
]