from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum
from .models import Categoria,DetalleFactura, Producto, Venta, DetalleVenta, Proveedor, Favorito, Carrito, Factura, RegistroEntrada, CarritoItem,User

# Registrar los otros modelos
admin.site.register(Favorito)
admin.site.register(Categoria)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Proveedor)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(Factura)
admin.site.register(RegistroEntrada)
admin.site.register(DetalleFactura)

# ProductoAdmin con la vista personalizada

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Otras configuraciones de ProductoAdmin

    def producto_mas_vendido_view(self, request):
        # Obtener el producto más vendido
        producto_mas_vendido = DetalleVenta.objects.values('producto__nombre').annotate(
            total_vendido=Sum('cantidad')
        ).order_by('-total_vendido').first()

        # Obtener el total de usuarios
        total_usuarios = User.objects.count()

        # Renderizar la plantilla con los datos
        return render(request, 'admin/producto_mas_vendido.html', {
            'producto_mas_vendido': producto_mas_vendido,
            'total_usuarios': total_usuarios
        })
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('producto-mas-vendido/', self.admin_site.admin_view(self.producto_mas_vendido_view), name='producto_mas_vendido'),
        ]
        return custom_urls + urls
