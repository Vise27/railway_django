from rest_framework import viewsets
from .models import Categoria, Empleado, Venta, Proveedor, Producto, DetalleVenta, Inventario,favorito
from .serializer import CategoriaSerializer, EmpleadoSerializer, VentaSerializer, ProveedorSerializer, ProductoSerializer, DetalleVentaSerializer, InventarioSerializer,FavoritoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class FavoritoViewSet(viewsets.ModelViewSet):
    queryset= favorito.objects.all()
    serializer_class= FavoritoSerializer


