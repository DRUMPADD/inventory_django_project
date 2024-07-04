from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(MyCustomUser)
class UserModelView(admin.ModelAdmin):
    list_display = ('username', 'name_user', 'middle_name', 'last_name', 'is_staff', 'is_superuser', 'is_active',)
    search_fields = ['username']
    list_filter = ['is_superuser', 'is_staff', 'is_active']
@admin.register(Proveedor)
class SupplierModelView(admin.ModelAdmin):
    list_display = ('folio', 'nombre',)
    search_fields = ['folio', 'nombre']

@admin.register(Producto)
class ProductModelView(admin.ModelAdmin):
    list_display = ('descripcion', 'cantidad', 'codigo', 'status', 'disponible',)
    search_fields = ['descripcion', 'codigo']
    list_filter = ['disponible', 'categoria']

@admin.register(Estados_de_producto)
class StateProductModelView(admin.ModelAdmin):
    list_display = ('producto', 'cantidad_disponible', 'estado', 'fecha_hora',)
    search_fields = ['producto__descripcion', 'condiciones', 'fecha_hora']
    list_filter = ['estado']

@admin.register(Movimiento)
class MovementsModelView(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'estado', 'fecha_salida', 'fecha_regreso',)
    search_fields = ['producto__producto__descripcion', 'fecha_salida', 'fecha_regreso']
    list_filter = ['estado', 'tipo_movimiento']
    
@admin.register(Historial)
class HistoryModelView(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'movimiento', 'fecha_hora',)
    search_fields = ['usuario', 'producto', 'descripcion']