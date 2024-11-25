from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum
from .models import Categoria,DetalleRegistroEntrada,RegistroSalida,DetalleRegistroSalida,DetalleFactura,Ubicacion, Producto, Venta, DetalleVenta, Proveedor, Favorito, Carrito, Factura, RegistroEntrada, CarritoItem,User

# Registrar los otros modelos

admin.site.register(DetalleRegistroSalida)
admin.site.register(Favorito)
admin.site.register(Ubicacion)
admin.site.register(Categoria)
admin.site.register(DetalleVenta)
admin.site.register(Proveedor)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(Factura)
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

class DetalleRegistroEntradaInline(admin.TabularInline):
    model = DetalleRegistroEntrada
    extra = 1  # Número de filas vacías adicionales para agregar nuevos detalles
    fields = ['producto', 'cantidad']
    verbose_name = "Detalle de Registro de Entrada"
    verbose_name_plural = "Detalles de Registro de Entrada"

@admin.register(RegistroEntrada)
class RegistroEntradaAdmin(admin.ModelAdmin):
    list_display = ['id_registro', 'proveedor', 'fecha']
    search_fields = ['proveedor__nombre']
    inlines = [DetalleRegistroEntradaInline]

# Inline para DetalleRegistroSalida
class DetalleRegistroSalidaInline(admin.TabularInline):
    model = DetalleRegistroSalida
    extra = 1  # Mostrar un formulario adicional
    autocomplete_fields = ['venta']  # Permitir autocompletar ventas


# Admin personalizado para RegistroSalida
@admin.register(RegistroSalida)
class RegistroSalidaAdmin(admin.ModelAdmin):
    inlines = [DetalleRegistroSalidaInline]
    list_display = ('id_registro', 'fecha_registro', 'descripcion')
    search_fields = ('descripcion',)
    list_filter = ('fecha_registro',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Automatizar detalles en un nuevo registro
            ventas_pendientes = Venta.objects.filter(estado='pendiente')
            for venta in ventas_pendientes:
                DetalleRegistroSalida.objects.create(registro_salida=obj, venta=venta)


# Acción personalizada para asociar ventas a un RegistroSalida
def asociar_a_registro_salida(modeladmin, request, queryset):
    registro_salida = RegistroSalida.objects.create(descripcion="Salida generada desde acción")
    for venta in queryset:
        DetalleRegistroSalida.objects.create(registro_salida=registro_salida, venta=venta)
        venta.estado = 'entregado'
        venta.save()

    modeladmin.message_user(request, f"RegistroSalida {registro_salida.id_registro} creado con {queryset.count()} ventas.")


asociar_a_registro_salida.short_description = "Asociar ventas seleccionadas a un Registro de Salida"


# Admin personalizado para Venta
@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'usuario', 'estado', 'total', 'fecha']
    search_fields = ['codigo', 'usuario__username', 'estado']
    list_filter = ['estado', 'fecha']
    actions = [asociar_a_registro_salida]

    def get_queryset(self, request):
        # Llamar al queryset original y filtrar las ventas pendientes
        queryset = super().get_queryset(request)
        return queryset.filter(estado='pendiente')
