from django.db.models import Sum
from .models import DetalleVenta,Venta

def producto_mas_vendido():
    return DetalleVenta.objects.values('producto__nombre').annotate(total_vendido=Sum('cantidad')).order_by('-total_vendido').first()

def usuario_mas_compras():
    return Venta.objects.values('usuario__username').annotate(total_compras=Sum('total')).order_by('-total_compras').first()
