from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('agregar/<int:articulo_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:articulo_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar/', views.actualizar_carrito, name='actualizar_carrito'),
    path('pedido/', views.colocar_pedido, name='colocar_pedido'),
]
