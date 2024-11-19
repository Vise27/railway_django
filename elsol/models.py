from django.contrib.auth.models import User 
from django.db import models
from django.utils import timezone
from django.conf import settings  # Agregar importación de settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Categoria(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.tipo

class Proveedor(models.Model):
    id = models.BigAutoField(primary_key=True)
    correo = models.EmailField(max_length=255, null=True) 
    direccion = models.CharField(max_length=255, null=True)
    nombre = models.CharField(max_length=255, null=True)
    telefono = models.CharField(max_length=20, null=True) 

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    imagen = models.ImageField(upload_to='imagenes_productos/', null=True)  
    nombre = models.CharField(max_length=255, null=True)
    precio = models.FloatField(null=True)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    @property
    def imageUrl(self):
        if self.imagen:
            return f"{settings.MEDIA_URL}{self.imagen.url}"  # Corregir para usar .url
        return ''

class Carrito(models.Model):
    id_carrito = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(default=timezone.now)  # Usar default en lugar de auto_now_add
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito {self.id_carrito} - Usuario: {self.usuario.username}"

    @property
    def total_carrito(self):
        items = self.items.all()
        return sum(item.cantidad * item.producto.precio for item in items)

class CarritoItem(models.Model):
    id_item = models.BigAutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item: {self.producto.nombre} - Cantidad: {self.cantidad}"

    @property
    def total_precio(self):
        return self.cantidad * self.producto.precio

    def save(self, *args, **kwargs):
        # Verificar si hay suficiente stock antes de guardar
        if self.cantidad > self.producto.stock:
            raise ValueError(f"Solo hay {self.producto.stock} unidades disponibles del producto {self.producto.nombre}.")
        super().save(*args, **kwargs)

class Venta(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta {self.codigo} - Total: {self.total} - Usuario: {self.usuario.username}"

    def save(self, *args, **kwargs):
        # Calcular el total basado en los items del carrito
        if not self.total:
            self.total = self.carrito.total_carrito
        super().save(*args, **kwargs)

class Favorito(models.Model):
    id = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorito {self.id} - Producto: {self.producto.nombre} - Usuario: {self.usuario.username}"

class DetalleVenta(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()  
    precio_unitario = models.FloatField(null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)

    def __str__(self):
        return f"Detalle de Venta {self.codigo} - Producto: {self.producto.nombre}"

class Factura(models.Model):
    id_factura = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)

    def __str__(self):
        return f"Factura {self.id_factura} - Usuario: {self.usuario.username}"

class RegistroEntrada(models.Model):
    id_registro = models.BigAutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Registro Entrada {self.id_registro} - Producto: {self.producto.nombre} - Cantidad: {self.cantidad}"

# Señal para actualizar el stock del producto
@receiver(post_save, sender=RegistroEntrada)
def actualizar_stock(sender, instance, **kwargs):
    producto = instance.producto
    producto.stock += instance.cantidad
    producto.save()

@receiver(post_save, sender=User)
def crear_carrito_usuario(sender, instance, created, **kwargs):
    if created:  # Si el usuario fue creado
        # Crear un carrito asociado al usuario recién creado
        Carrito.objects.create(usuario=instance)
