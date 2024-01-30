from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager, ProductModelManager, SaleModelManager, RentModelManager
# Create your models here.

class MyCustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=255, unique=True)
    name_user = models.CharField(max_length=255, default='')
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name_user','middle_name', 'last_name']
    
    def __str__(self) -> str:
        return f'{self.username}'



'''
Productos
Proveedor
Usuario
Renta
Venta
Historial
'''


class Proveedor(models.Model):
    folio = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.folio

class Producto(models.Model):
    def __str__(self) -> str:
        return f'{self.pk}'
    
    descripcion = models.CharField(max_length=255)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.FloatField(default=1)
    tamanio = models.FloatField(default=0, blank=True)
    libraje = models.FloatField(default=0, blank=True)
    conexion = models.CharField(max_length=10, blank=True)
    unidad_medida = models.CharField(max_length=100, default="", null=True)
    conexion_medida = models.CharField(max_length=10, blank=True)
    codigo = models.CharField(max_length=20, null=True)
    no_serie = models.CharField(max_length=10, blank=True)
    no_serie_interno = models.CharField(max_length=10, blank=True)
    orden_compra = models.CharField(max_length=10, blank=True)
    tipo_orden_compra = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=40, blank=True)
    pozo = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)
    modelo = models.CharField(max_length=100, blank=True, default="")
    marca = models.CharField(max_length=100, blank=True, default="")
    area = models.CharField(max_length=100, blank=True, default="")
    proyecto = models.CharField(max_length=200, blank=True, default="")
    resguardo = models.CharField(max_length=100, blank=True, null=True, default="")
    categoria = models.CharField(max_length=15, blank=True) # Herramienta o equipo
    disponible = models.BooleanField(default=True)
    objects = models.Manager()
    products = ProductModelManager()


class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_salida = models.DateField(null=True, blank=True)
    objects = models.Manager()
    sales = SaleModelManager()

class Renta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=0)
    fecha_salida = models.DateField(null=True, blank=True)
    fecha_regreso = models.DateField(null=True, blank=True)
    objects = models.Manager()
    rents = RentModelManager()

class Historial(models.Model):
    usuario = models.ForeignKey(MyCustomUser, on_delete=models.CASCADE)
    descripcion = models.TextField()
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, null=True, blank=True)
    renta = models.ForeignKey(Renta, on_delete=models.CASCADE, null=True, blank=True)
    fecha_hora = models.DateTimeField(default=timezone.now)

    def get_history(self):
        return self.objects.all().values("pk", "venta", "renta", "descripcion", "fecha_hora", "usuario", "usuario__name_user", "venta__producto__descripcion", "renta__producto__descripcion")