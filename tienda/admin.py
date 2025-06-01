from django.contrib import admin
from .models import Cliente, Articulo, Carrito, ItemCarrito, Pedido, PedidoItem

admin.site.register(Cliente)
admin.site.register(Articulo)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Pedido)
admin.site.register(PedidoItem)

