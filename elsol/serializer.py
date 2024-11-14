from rest_framework import serializers
from .models import Categoria, Empleado, Venta, Proveedor, Producto, DetalleVenta, Inventario, favorito
from django.contrib.auth.models import User


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__' 


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'  


class VentaSerializer(serializers.ModelSerializer):
    empleado = EmpleadoSerializer() 
    usuario = serializers.StringRelatedField()  

    class Meta:
        model = Venta
        fields = '__all__'  


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__' 


class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()  
    proveedor = ProveedorSerializer()  


    class Meta:
        model = Producto
        fields = '__all__'  


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer() 
    venta = VentaSerializer()  

    class Meta:
        model = DetalleVenta
        fields = '__all__'  


class InventarioSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer() 

    class Meta:
        model = Inventario
        fields = '__all__' 
        
class FavoritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  
    usuario = serializers.StringRelatedField()  

    class Meta:
        model = favorito
        fields = '__all__'