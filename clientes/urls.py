from django.urls import path
from .views import NuevoClienteCreateView, ClientesList110Json

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
   path('cliente/nuevo', NuevoClienteCreateView.as_view(), name='nuevo_cliente'),
   path('clientes_data_110/', ClientesList110Json.as_view(), name="listar_clientes"),#ajax
   path('', LoginView.as_view(template_name='accounts/login.html'), name='login'),
   path('logoutsesion/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
 
]