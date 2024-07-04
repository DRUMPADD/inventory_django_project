from django.db import models
from datetime import date
from django.db.models import Exists, OuterRef
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def __str__(self) -> str:
        return f'{self.username}'
    
    def create_user(self, username, name_user, middle_name, last_name, password=None):
        if not username:
            raise ValueError("El usuario debe tener un correo electrónico")
        if not password:
            raise ValueError("La contraseña es requerida")
        
        user = self.model(
            username=username,
            name_user=name_user,
            middle_name=middle_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, name_user, middle_name, last_name, password=None):
        user = self.create_user(
            username=username,
            name_user=name_user,
            middle_name=middle_name,
            last_name=last_name,
            password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class ProductModelManager(models.Manager):
    def get_items(self) -> models.QuerySet:
        return self.get_queryset().filter(categoria='HERRAMIENTA')

    def get_tools(self) -> models.QuerySet:
        return self.get_queryset().filter(categoria='EQUIPO')
    
    def get_codes(self, category: str) -> models.QuerySet:
        return self.get_queryset().filter(disponible=True, categoria=category).values('codigo').annotate(code=models.Count('codigo')).order_by('code')
    
    def filter_products_available(self, movements_model: models.Model):
        return self.get_queryset().annotate(no_products_with_movement=~Exists(movements_model.objects.filter(producto=OuterRef("pk")))).filter(no_products_with_movement=True, categoria="HERRAMIENTA", disponible=True).values("pk", "descripcion", "tamanio")

    
    def create_product(self, model_supplier: models.Model, data: object) -> int:
        try:
            check_provider = model_supplier.objects.get(folio=data.get("proveedor"))
        except (model_supplier.DoesNotExist, model_supplier.MultipleObjectsReturned):
            check_provider = ""
        if data.get("categoria") == 'HERRAMIENTA': id = self.get_queryset().create(descripcion=data.get("producto"), tamanio=data.get("tamanio"), cantidad=float(data.get("cantidad")) if data.get("cantidad") != "" else 1, libraje=float(data.get("libraje")), conexion=data.get("conexion"), conexion_medida=data.get("medida"), no_serie=data.get("noserie"), orden_compra=data.get("oc"), status=data.get("status"), tipo_orden_compra=data.get("sl_opcion_oc"), proveedor=check_provider if check_provider != "" else None, no_serie_interno=data.get("noseriei"), categoria="HERRAMIENTA", pozo=data.get("pozo"), observaciones=data.get("observaciones"), codigo=data.get("codigo"))
        else: id = self.get_queryset().create(descripcion=data.get("producto"), area=data.get("area"), marca=data.get("marca"), modelo=data.get("modelo"), proyecto=data.get("proyecto"), resguardo=data.get("resguardo"), orden_compra=data.get("oc"), status=data.get("status"), no_serie=data.get("noserie"), tipo_orden_compra=data.get("sl_opcion_oc"), proveedor=check_provider if check_provider != "" else None, no_serie_interno=data.get("noseriei"), cantidad=float(data.get("cantidad")) if data.get("cantidad") != "" else 1, categoria="EQUIPO", tamanio=data.get("tamanio"))
        return id
        
    def create_tool(self, model_supplier: models.Model, data: object) -> int:
        try:
            check_provider = model_supplier.objects.get(folio=data.get("proveedor"))
        except (model_supplier.DoesNotExist, model_supplier.MultipleObjectsReturned):
            check_provider = ""
        if data.get("categoria") == 'HERRAMIENTA':
            id = self.get_queryset().create(descripcion=data.get("herramienta"), tamanio=data.get("tamanio"), cantidad=float(data.get("cantidad")) if data.get("cantidad") != "" else 1, libraje=float(data.get("libraje")), conexion=data.get("conexion"), conexion_medida=data.get("medida"), no_serie=data.get("noserie"), orden_compra=data.get("oc"), status=data.get("status"), tipo_orden_compra=data.get("sl_opcion_oc"), proveedor=check_provider if check_provider != "" else None, no_serie_interno=data.get("noseriei"), categoria="HERRAMIENTA", pozo=data.get("pozo"), observaciones=data.get("observaciones"), codigo=data.get("codigo"))
        else: id = self.get_queryset().create(descripcion=data.get("articulo"), area=data.get("area"), marca=data.get("marca"), modelo=data.get("modelo"), proyecto=data.get("proyecto"), resguardo=data.get("resguardo"), orden_compra=data.get("oc"), status=data.get("status"), no_serie=data.get("noserie"), tipo_orden_compra=data.get("sl_opcion_oc"), proveedor=check_provider if check_provider != "" else None, no_serie_interno=data.get("noseriei"), cantidad=float(data.get("cantidad")) if data.get("cantidad") != "" else 1, categoria="EQUIPO", tamanio=data.get("tamanio"))
        return id.descripcion
    
    def create_item(self, model_supplier: models.Model, data: object) -> int:
        try:
            check_provider = model_supplier.objects.get(folio=data.get("proveedor"))
        except (model_supplier.DoesNotExist, model_supplier.MultipleObjectsReturned):
            check_provider = ""
        id = self.get_queryset().create(descripcion=data.get("articulo"), area=data.get("area"), marca=data.get("marca"), modelo=data.get("modelo"), proyecto=data.get("proyecto"), resguardo=data.get("resguardo"), orden_compra=data.get("oc"), status=data.get("status"), no_serie=data.get("noserie"), tipo_orden_compra=data.get("sl_opcion_oc"), proveedor=check_provider if check_provider != "" else None, no_serie_interno=data.get("noseriei"), cantidad=float(data.get("cantidad")) if data.get("cantidad") != "" else 1, categoria="EQUIPO", tamanio=data.get("tamanio"))
        return id.pk

    def update_tool(self, model_supplier: models.Model, id_tool: int, data: object) -> str:
        name_before = self.get_queryset().filter(pk=id_tool).values("descripcion")
        self.get_queryset().filter(pk=id_tool).update(descripcion=data.get("producto"), tamanio=data.get("tamanio"), cantidad=float(data.get("cantidad")), libraje=data.get("libraje"), conexion=data.get("conexion"), conexion_medida=data.get("medida"), no_serie=data.get("noserie"), orden_compra=data.get("oc"), status=data.get("status"), tipo_orden_compra=data.get("sl_opcion_oc"), proveedor=model_supplier.objects.get(folio=data.get("proveedor")) if data.get("proveedor") else None, no_serie_interno=data.get("noseriei"), pozo=data.get("pozo"), observaciones=data.get("observaciones"), codigo=data.get("codigo"))
        return name_before[0]["descripcion"]
    
    def update_item(self, model_supplier: models.Model, id_item: int, data: object) -> str:
        print(data.get("codigo"))
        name_before = self.get_queryset().filter(pk=id_item).values("descripcion")
        self.get_queryset().filter(pk=id_item).update(descripcion=data.get("producto"), cantidad=float(data.get("cantidad")), area=data.get("area"), marca=data.get("marca"), modelo=data.get("modelo"), proyecto=data.get("proyecto"), resguardo=data.get("resguardo"), orden_compra=data.get("oc"), status=data.get("status"), no_serie=data.get("noserie"), tipo_orden_compra=data.get("sl_opcion_oc"), proveedor=model_supplier.objects.get(folio=data.get("proveedor")) if data.get("proveedor") else None, no_serie_interno=data.get("noseriei"), tamanio=data.get("tamanio"))
        return name_before[0]["descripcion"]
    
    def delete_product(self, id_product: int):
        self.get_queryset().filter(pk=id_product).update(disponible=False)
        return self.get_queryset().get(pk=id_product).disponible
    
    def get_item_info(self, id_item: int) -> models.QuerySet:
        return self.get_queryset().filter(pk=id_item).values("pk", "descripcion", "area", "marca", "modelo", "proyecto", "resguardo", "proveedor__folio", "proveedor__nombre", "orden_compra", "no_serie", "tipo_orden_compra", "no_serie_interno", "categoria", "status", "tamanio", "cantidad")

    def get_tool_info(self, id_tool: int) -> models.QuerySet:
        return self.get_queryset().filter(pk=id_tool).values("pk", "descripcion", "tamanio", "libraje", "conexion", "conexion_medida", "proveedor__folio", "proveedor__nombre", "orden_compra", "codigo", "tipo_orden_compra", "no_serie", "no_serie_interno", "categoria", "pozo", "observaciones", "status", "cantidad")
    
    def filter_products_by_name_size(self, state_product_model: models.Model, category: str):
        return self.get_queryset().values("descripcion", "tamanio").order_by("descripcion", "tamanio").annotate(total=models.Sum("cantidad"), no_products_with_move=~Exists(state_product_model.objects.filter(producto=OuterRef("pk")))).filter(no_products_with_move=True, categoria=category)

class TransactionsManager(models.Manager):
    def __str__(self) -> str:
        return f'{self.pk} {self.producto}'

    # ? Rentas
    def get_rent_info(self, rent_pk: int):
        return self.get_queryset().filter(pk=rent_pk).values("pk", "producto__producto__pk", "producto__producto__descripcion", "producto__producto__categoria", "fecha_salida", "fecha_regreso", "cantidad", "tipo_movimiento", "estado")
    
    def get_all_products_rented(self) -> models.QuerySet:
        return self.get_queryset().filter(tipo_movimiento='RENTA').values("pk", "producto__pk", "producto__producto__descripcion", "producto__producto__no_serie", "fecha_salida", "fecha_regreso", "producto__producto__categoria", "cantidad", "tipo_movimiento")
    
    def filter_products_rented(self, category: str):
        return self.get_queryset().filter(producto__producto__categoria=category, tipo_movimiento='RENTA').values("pk", "producto__producto__pk", "producto__producto__descripcion", "producto__producto__tamanio")

    def filter_products_by_name_size_rented(self, category: str):
        return self.get_queryset().filter(producto__producto__categoria=category, tipo_movimiento='RENTA').annotate(models.Count("producto__producto__descripcion"), models.Count("producto__producto__tamanio"), total=models.Sum("cantidad")).values('pk', "producto__producto__descripcion", "producto__producto__tamanio", "total")
    
    def register_rent(self, product_model: models.Model, id_product: int, object_date: dict):
        new_rent = self.get_queryset().create(producto=product_model.objects.get(pk=id_product), fecha_salida=object_date.get("fsalida") if object_date.get("fsalida") else None,  fecha_regreso=object_date.get("fregreso") if object_date.get("fregreso") else None, cantidad=object_date.get("cantidad"))
        return new_rent.pk
    
    def today(self):
        return date.today()
    
    def update_rent(self, id: int, info: dict):
        rent = self.get_queryset().get(pk=id)
        rent.fecha_salida = info.get("fsalida") if info.get("fsalida") else None, 
        rent.fecha_regreso = info.get("fregreso") if info.get("fregreso") else None, 
        rent.cantidad = float(info.get("cantidad"))
        return rent
    
    # ? Ventas
    def get_all_products_sold(self) -> models.QuerySet:
        return self.get_queryset().filter(tipo_movimiento='VENTA').values("pk", "producto__producto__pk", "producto__producto__descripcion", "producto__producto__no_serie", "fecha_salida", "cantidad", "producto__producto__categoria")

    def get_sale_info(self, sale_pk: int):
        return self.get_queryset().filter(pk=sale_pk).values("pk", "producto__producto__pk", "producto__producto__descripcion", "producto__producto__categoria", "fecha_salida", "cantidad", "tipo_movimiento", "estado")
    
    def filter_products_sold(self, category: str):
        return self.get_queryset().filter(producto__producto__categoria=category, tipo_movimiento='VENTA').values("pk", "producto__producto__pk", "producto__producto__descripcion", "producto__producto__tamanio")
    
    def register_sale(self, product_model: models.Model, info_prod: object, object_date: dict, user):
        new_sale = self.get_queryset().create(producto=product_model.objects.get(pk=info_prod.get("id_product")), fecha_salida=object_date.get("fsalida") if object_date.get("fsalida") else None, usuario=user, cantidad=float(info_prod.get("cantidad")))
        return new_sale.pk

    def update_sale(self, id: int, info: dict):
        self.get_queryset().filter(pk=id).update(fecha_salida=info.get("fsalida") if info.get("fsalida") else None, cantidad=float(info.get("cantidad")))

    def create_rent_or_sale(self, product: models.Model, info: object, types_mov: models.Model, user: models.Model, status: models.Model):
        if types_mov.nombre == 'VENTA':
            new_movement = self.get_queryset().create(
                producto=product, 
                fecha_salida=info.get("fsalida") if info.get("fsalida") else None, 
                usuario=user, 
                cantidad=float(info.get("cantidad")),
                tipo_movimiento=types_mov,
                estado=status)
        else:
            new_movement = self.get_queryset().create(
                producto=product, 
                fecha_salida=info.get("fsalida") if info.get("fsalida") else None, 
                fecha_regreso=info.get("fregreso") if info.get("fregreso") else None, 
                cantidad=float(info.get("cantidad")), 
                usuario=user,
                tipo_movimiento=types_mov,
                estado=status)
        return new_movement.pk
    
    def create_use_of_product(self, info: object, product: models.Model, user: models.Model, types_mov: models.Model, status: models.Model):
        product = self.get_queryset().create(
            producto = product,
            cantidad = float(info.get("cantidad")),
            tipo_movimiento = types_mov,
            estado = status,
            condicion = info.get("condicion"),
            usuario = user,
        )
        return product

class HistoryChangeManager(models.Manager):
    def __str__(self) -> str:
        return self.pk
    
    def get_all_changes_product(self, id_transaction: int):
        return self.get_queryset().filter(movimiento=id_transaction)

class StateProductManager(models.Manager):
    def dispose_product(self, product: models.Model, info: object):
        use = self.get_queryset().create(
            producto=product,
            cantidad_disponible=float(info.get("cantidad")),
            condiciones=info.get("condiciones"),
            estado=info.get("estado"),
        )
        return use

'''
registrar venta de producto
registrar renta de producto
registrar uso de producto
'''