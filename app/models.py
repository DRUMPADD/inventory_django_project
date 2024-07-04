from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# from django.utils import timezone
from .managers import CustomUserManager, ProductModelManager, TransactionsManager, HistoryChangeManager, StateProductManager
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
    
    class Meta:
        db_table = 'usuarios'

    def __str__(self) -> str:
        return f'{self.username}'


class Proveedor(models.Model):
    folio = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'proveedores'

    def __str__(self):
        return self.folio

class Producto(models.Model):
    def __str__(self) -> str:
        return f'{self.pk}.- {self.descripcion}'
    
    descripcion = models.CharField(max_length=255)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.FloatField(default=1)
    tamanio = models.CharField(max_length=20, default=0, blank=True)
    libraje = models.FloatField(default=0, blank=True)
    conexion = models.CharField(max_length=10, blank=True)
    unidad_medida = models.CharField(max_length=100, default="", null=True)
    conexion_medida = models.CharField(max_length=10, blank=True)
    codigo = models.CharField(max_length=20, null=True)
    no_serie = models.CharField(max_length=50, blank=True)
    no_serie_interno = models.CharField(max_length=50, blank=True)
    orden_compra = models.CharField(max_length=200, blank=True)
    tipo_orden_compra = models.CharField(max_length=50, blank=True)
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

    class Meta:
        db_table = 'productos'

class Estados_de_producto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad_disponible = models.FloatField()
    estado = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    condiciones = models.TextField(default="")
    objects = models.Manager()
    uses = StateProductManager()

    class Meta:
        db_table = 'estados_producto'
    
    def __str__(self) -> str:
        return f'{self.producto}'


class Movimiento(models.Model):
    producto = models.ForeignKey(Estados_de_producto, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=50)
    cantidad = models.FloatField()
    estado = models.CharField(default="", max_length=60, null=True)
    fecha_salida = models.DateField(null=True, blank=True)
    fecha_regreso = models.DateField(null=True, blank=True)
    movements = TransactionsManager()
    objects = models.Manager()

    class Meta:
        db_table = 'movimientos'
    
    def __str__(self) -> str:
        return f'{self.pk}.- {self.producto.producto.descripcion}'

class Historial(models.Model):
    usuario = models.ForeignKey(MyCustomUser, on_delete=models.SET_NULL, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'historial'

    def get_history(self):
        return self.objects.all().values("pk", "descripcion", "fecha_hora", "usuario", "usuario__name_user", "producto__descripcion")