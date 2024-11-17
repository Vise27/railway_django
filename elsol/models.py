from django.contrib.auth.models import User
from django.db import models

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
            return f"{settings.MEDIA_URL}{self.imagen}"
        return ''
class Carrito(models.Model):
    id_carrito = models.BigAutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Carrito {self.id_carrito} - Producto: {self.producto.nombre} - Usuario: {self.usuario.username}"

class Venta(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.FloatField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Venta {self.codigo} - Total: {self.total} - Usuario: {self.usuario.username} - Carrito: {self.carrito.id_carrito}"



class favorito(models.Model):
    id=models.BigIntegerField(primary_key=True)
    producto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    User=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"favorito{self.id} - Producto: {self.producto.nombre}- Usuario: {self.User.last_name}"
    
class DetalleVenta(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()  
    precio_unitario = models.FloatField(null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)

    def __str__(self):
        return f"Detalle de Venta {self.codigo} - Producto: {self.producto.nombre}"


class Inventario(models.Model):
    id_inventario = models.BigAutoField(primary_key=True)
    cantidad = models.PositiveIntegerField(default=0) 
    fecha = models.DateTimeField(auto_now_add=True)  
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventario de {self.producto.nombre} - Cantidad: {self.cantidad}"
    


class Factura(models.Model):
    id_factura = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Factura {self.id_factura} - Usuario: {self.usuario.username} - Carrito: {self.carrito.id_carrito}"
    
class Registro_entrada(models.Model):
    id_reegitro = models.BigAutoField(primary_key=True)
    provedor =  models.ForeignKey(Proveedor,on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)