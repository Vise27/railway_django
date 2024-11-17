from rest_framework import serializers
from .models import Categoria, Venta, Proveedor, Producto, DetalleVenta, Inventario, favorito, Factura, Carrito
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['username']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()  # Incluye la información de la categoría
    proveedor = ProveedorSerializer()  # Incluye la información del proveedor

    class Meta:
        model = Producto
        fields = '__all__'



class VentaSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()  # Incluye el nombre del usuario relacionado

    class Meta:
        model = Venta
        fields = '__all__'


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Relación con Producto
    venta = VentaSerializer()  # Relación con Venta

    class Meta:
        model = DetalleVenta
        fields = '__all__'


class InventarioSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Relación con Producto

    class Meta:
        model = Inventario
        fields = '__all__'


class FavoritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Relación con Producto
    usuario = serializers.StringRelatedField()  # Relación con Usuario

    class Meta:
        model = favorito
        fields = '__all__'


class CarritoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()  
    producto = ProductoSerializer() 
    cantidad = serializers.IntegerField()  
    total = serializers.DecimalField(max_digits=10, decimal_places=2)  

    class Meta:
        model = Carrito
        fields = '__all__'


class FacturaSerializer(serializers.ModelSerializer):
    venta = VentaSerializer()  # Relación con Venta
    usuario = serializers.StringRelatedField()  # Relación con el usuario (nombre de usuario)

    class Meta:
        model = Factura
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
