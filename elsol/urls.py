from django.urls import path, include
from rest_framework import routers
from .views import (
    UserProfileView, CarritoViewSet, CarritoItemViewSet, FacturaViewSet, 
    CustomTokenObtainPairView, RegisterUserView, CategoriaViewSet, 
    FavoritoViewSet, VentaViewSet, ProveedorViewSet, ProductoViewSet, DetalleVentaViewSet
)

router = routers.DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'detalles-venta', DetalleVentaViewSet)
router.register(r'favoritos', FavoritoViewSet)
#router.register(r'carritos', CarritoViewSet)#por mientra no esta en uso
#router.register(r'carrito-items', CarritoItemViewSet) #por mientras no esta en uso
router.register(r'facturas', FacturaViewSet)

urlpatterns = [
    path('', include(router.urls)), 
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
]
