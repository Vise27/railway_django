from django.contrib import admin

# Register your models here.

from.models import Categoria,Producto,Venta,DetalleVenta,Proveedor,favorito,Carrito,Factura,Registro_entrada



admin.site.register(favorito)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Proveedor)
admin.site.register(Carrito)
admin.site.register(Factura)
admin.site.register(Registro_entrada)

