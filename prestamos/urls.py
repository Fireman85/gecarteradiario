
from django.urls import path
from .views import home, nuevo_Prestamo,autocompleteModel,traerDatosdeCliente, nuevo_Abono, UsersList110Json,PrestamosList110Json,AbonosList110Json,registrar_abono,nuevo_union_cuentas,PrestamosTodosList110Json,borrar_Prestamo,borrar_Abono,mostrar_estado_cuenta,descuento_Prestamo,registrar_descuento,DescuentosList110Json,borrar_Descuento

urlpatterns = [
   path('inicio/', home, name='home'),
   path('prestamo/nuevo/', nuevo_Prestamo, name='nuevoPrestamo'), #ajax
   path('prestamo/descuento/', descuento_Prestamo, name='descuentoPrestamo'), #ajax copia de abono nuevo
   path('prestamo/borrar/', borrar_Prestamo, name='borrarPrestamo'), #ajax
   path('abono/borrar/', borrar_Abono, name='borrarAbono'), #ajax
   path('descuento/borrar/', borrar_Descuento, name='borrarDescuento'), #ajax
   path('abono/nuevo', nuevo_Abono, name='nuevoAbono'),
   path('unioncuentas/nuevo/', nuevo_union_cuentas, name='nuevo_union_cuen'),
   path('ajax_calls/search/', autocompleteModel, name='search'),
   path('ajax_calls/traerDatosdeCliente/', traerDatosdeCliente, name='traerDatosdeCliente'),#ajax
   path('ajax_calls/registrarAbono/', registrar_abono, name='registrar_abono'),#ajax
   path('ajax_calls/registrarDescuento/', registrar_descuento, name='registrar_descuento'),#ajax
   path('users_data_110/', UsersList110Json.as_view(), name="UsersList110Json"),#ajax
   path('prestamos_data_110/', PrestamosList110Json.as_view(), name="PrestamosList110Json"),#ajax
   path('abonos_data_110/', AbonosList110Json.as_view(), name="AbonosList110Json"),#ajax
   path('descuentos_data_110/', DescuentosList110Json.as_view(), name="DescuentosList110Json"),#ajax
   path('prestamos_todos_110/', PrestamosTodosList110Json.as_view(), name="listar_prestamos_todos"),#ajax
   path('prestamo/estadocuenta/', mostrar_estado_cuenta, name="mostrar_estado_cuenta_cliente"),
]