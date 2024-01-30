from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.MyCustomUser)
class CustomUserModelView(admin.ModelAdmin):
    model = models.MyCustomUser
    list_display = ('username', 'name_user','middle_name', 'last_name', 'password', 'is_superuser', 'is_staff', 'is_active')

@admin.register(models.Producto)
class ProductModelView(admin.ModelAdmin):
    model = models.Producto
    list_display = ('pk', 'descripcion', 'codigo', 'cantidad', 'proveedor', 'tamanio', 'libraje', 'conexion', 'conexion_medida', 'no_serie', 'no_serie_interno', 'orden_compra', 'tipo_orden_compra', 'status', 'pozo', 'observaciones', 'modelo', 'marca', 'area','resguardo','categoria', 'disponible')

@admin.register(models.Proveedor)
class ProductModelView(admin.ModelAdmin):
    model = models.Proveedor
    list_display = ('folio', 'nombre')

@admin.register(models.Venta)
class SaleModelView(admin.ModelAdmin):
    model = models.Venta
    list_display = ('pk', 'producto')

@admin.register(models.Renta)
class RentModelView(admin.ModelAdmin):
    model = models.Renta
    list_display = ('pk', 'producto')

@admin.register(models.Historial)
class RentModelView(admin.ModelAdmin):
    model = models.Historial
    list_display = ('usuario', 'descripcion', 'venta', 'renta', 'fecha_hora')