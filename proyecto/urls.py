"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static
from elsol import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ventas_categorias',views.ventas_por_categoria,name='ventas_categorias'),
    path('ventas-mes',views.ventas_por_mes,name='ventas_mes'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('productos_sin_stock',views.productos_sin_stock,name='productos_sin_stock'),
    path('api/',include('elsol.urls')),
]

# Para la img
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

