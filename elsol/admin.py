from django.contrib import admin

# Register your models here.

from.models import Empleado,Categoria,Producto,Venta,DetalleVenta,Proveedor,Inventario,favorito



admin.site.register(favorito)
admin.site.register(Empleado)
#admin.site.register(User)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Proveedor)
admin.site.register(Inventario)

