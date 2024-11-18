from django.contrib import admin

# Register your models here.

from.models import Categoria,Producto,Venta,DetalleVenta,Proveedor,Favorito,Carrito,Factura,RegistroEntrada,CarritoItem


admin.site.register(Favorito)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Proveedor)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(Factura)
admin.site.register(RegistroEntrada)

