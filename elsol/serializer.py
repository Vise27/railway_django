from rest_framework import serializers
from .models import (
    Categoria, Venta, Proveedor, Producto, DetalleVenta, 
    Favorito, Factura, Carrito, CarritoItem
)
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

class FavoritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Relación con Producto
    usuario = serializers.StringRelatedField()  # Relación con Usuario

    class Meta:
        model = Favorito  # Corregido de 'favorito' a 'Favorito'
        fields = '__all__'

class CarritoItemSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())  # Relacionar solo con el ID del producto
    carrito = serializers.PrimaryKeyRelatedField(queryset=Carrito.objects.all())  # Relacionar con el carrito

    class Meta:
        model = CarritoItem
        fields = ['id_item', 'producto', 'cantidad', 'total_precio', 'carrito']

    def create(self, validated_data):
        producto = validated_data['producto']
        cantidad = validated_data['cantidad']
        carrito = validated_data['carrito']

        # Crear un nuevo CarritoItem
        carrito_item = CarritoItem.objects.create(
            producto=producto,
            cantidad=cantidad,
            carrito=carrito
        )
        # El cálculo del total_precio se realiza automáticamente al acceder a la propiedad
        return carrito_item

class CarritoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()  # Mostrar los detalles del usuario
    items = CarritoItemSerializer(many=True, read_only=True)  # Mostrar los items del carrito
    total_carrito = serializers.ReadOnlyField()  # Corregido: no es necesario el 'source'

    class Meta:
        model = Carrito
        fields = ['id_carrito', 'usuario', 'items', 'total_carrito', 'creado_en', 'actualizado_en']

class VentaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()  # Mostrar detalles del usuario
    carrito = CarritoSerializer()  # Mostrar detalles del carrito

    class Meta:
        model = Venta
        fields = '__all__'

    def create(self, validated_data):
        carrito_data = validated_data.pop('carrito', None)
        if carrito_data:
            carrito = Carrito.objects.get(id_carrito=carrito_data['id_carrito'])
            validated_data['total'] = carrito.total_carrito
        return super().create(validated_data)

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Relación con Producto

    class Meta:
        model = DetalleVenta
        fields = ['codigo', 'producto', 'cantidad', 'precio_unitario', 'venta']

class FacturaSerializer(serializers.ModelSerializer):
    carrito = CarritoSerializer()
    usuario = UserSerializer()

    class Meta:
        model = Factura
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
