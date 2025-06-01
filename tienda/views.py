from django.shortcuts import render, redirect, get_object_or_404
from .models import Articulo, Pedido, PedidoItem
from django.contrib.auth.models import User

# --- Vista del catálogo de artículos ---
def catalogo(request):
    articulos = Articulo.objects.all()
    carrito = obtener_carrito(request)
    items = []
    total = 0

    for id, cantidad in carrito.items():
        articulo = get_object_or_404(Articulo, pk=id)
        total_articulo = articulo.precio * cantidad
        items.append({'articulo': articulo, 'cantidad': cantidad, 'total': total_articulo})
        total += total_articulo

    return render(request, 'tienda/catalogo.html', {
        'articulos': articulos,
        'carrito': items,
        'total_carrito': total
    })


# --- Sesión como carrito temporal ---
def obtener_carrito(request):
    return request.session.get('carrito', {})

def guardar_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True

# --- Agregar al carrito ---
def agregar_al_carrito(request, articulo_id):
    carrito = obtener_carrito(request)
    carrito[str(articulo_id)] = carrito.get(str(articulo_id), 0) + 1
    guardar_carrito(request, carrito)
    return redirect('catalogo')

# --- Mostrar carrito ---
def ver_carrito(request):
    carrito = obtener_carrito(request)
    items = []
    total = 0

    for id, cantidad in carrito.items():
        articulo = get_object_or_404(Articulo, pk=id)
        total_articulo = articulo.precio * cantidad
        items.append({'articulo': articulo, 'cantidad': cantidad, 'total': total_articulo})
        total += total_articulo

    return render(request, 'tienda/carrito.html', {'carrito': items, 'total_carrito': total})

# --- Eliminar del carrito ---
def eliminar_del_carrito(request, articulo_id):
    carrito = obtener_carrito(request)
    carrito.pop(str(articulo_id), None)
    guardar_carrito(request, carrito)
    return redirect('ver_carrito')

# --- Actualizar cantidades ---
def actualizar_carrito(request):
    if request.method == 'POST':
        carrito = obtener_carrito(request)
        for key in carrito.keys():
            nueva_cantidad = request.POST.get(f'cantidad_{key}')
            if nueva_cantidad:
                carrito[key] = int(nueva_cantidad)
        guardar_carrito(request, carrito)
    return redirect('ver_carrito')

# --- Colocar pedido ---
def colocar_pedido(request):
    if request.method == 'POST':
        carrito = obtener_carrito(request)
        if not carrito:
            return redirect('ver_carrito')

        # Cliente actual (ejemplo: usuario logueado o asignación temporal)
        cliente = request.user if request.user.is_authenticated else User.objects.first()

        pedido = Pedido.objects.create(cliente=cliente, estatus='pendiente')
        for id, cantidad in carrito.items():
            articulo = Articulo.objects.get(pk=id)
            PedidoItem.objects.create(pedido=pedido, articulo=articulo, cantidad=cantidad)

        # Limpiar carrito
        request.session['carrito'] = {}
        return redirect('catalogo')
    return redirect('ver_carrito')
