from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError, FieldError, ObjectDoesNotExist
from django.db import IntegrityError, OperationalError, InternalError
from .. import models
import json

# ?? States of product
@require_http_methods(["PUT"])
@login_required(login_url="app:signin")
def update_use_of_product(request: HttpRequest, id_product: int, id_product_use: int) -> JsonResponse:
    '''
        Update state of product
    '''
    try:
        product = models.Producto.objects.get(pk=id_product)
        product_use = models.Movimientos.objects.get(pk=id_product_use)
        status = models.Estados.objects.get(pk=int(info.get("sl_status")))
        info = json.loads(request.body.decode("utf-8"))
        product_use.estado = status
        product_use.condicion = info.get("condicion")
        if float(info.get("cantidad_uso")) > product_use.cantidad_uso:
            if float(info.get("cantidad_uso")) - product_use.cantidad_uso < product.cantidad:
                product.cantidad = (product.cantidad + product_use.cantidad_uso) - float(info.get("cantidad_uso"))
                product_use.cantidad = float(info.get("cantidad_uso"))
            else:
                product_use.save()
                return JsonResponse({"message": "No hay suficiente equipo disponible", "status": 204}, status=204)
        if float(info.get("cantidad_uso")) < product_use.cantidad_uso:
            product.cantidad = (product_use.cantidad_uso - float(info.get("cantidad_uso"))) + product.cantidad
            product_use.cantidad = float(info.get("cantidad_uso"))
        if float(info.get("cantidad_uso")) == product_use.cantidad_uso and status.descripcion == 'Listo':
            product.cantidad = product.cantidad + float(info.get("cantidad_uso"))
        if status.descripcion == 'Listo':
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), producto=product, descripcion=f"Entrada de producto {product.descripcion} que estuvo en uso, cantidad actual: {product.cantidad}", cantidad_antes=product.cantidad+float(info.get("cantidad_uso")), cantidad_despues=product.cantidad)
            product_use.save()
            product.save()
            print(product.cantidad)
        else:
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), producto=product, descripcion=f"Actualización de producto {product.descripcion} en uso, cantidad actual: {product.cantidad}", cantidad_antes=product.cantidad+float(info.get("cantidad_uso")), cantidad_despues=product.cantidad)
            product_use.save()
            print(product_use)
            product.save()
        return JsonResponse({"message": "Actualización de equipo en uso", "status": 200}, status=200)
    except (json.JSONDecodeError, ValueError, ValidationError, FieldError, ObjectDoesNotExist, IntegrityError, OperationalError, InternalError):
        return JsonResponse({"message": "Error en el sistema", "status": 500}, status=500)

def edit_state_product(request: HttpRequest, id_product: int, id_product_state: int):
    try:
        product = models.Producto.objects.get(pk=id_product)
        state_product = models.Estados_de_producto.objects.get(pk=id_product_state)
        info_json = json.loads(request.body.decode('utf-8'))
        
        if product.cantidad + state_product.cantidad_disponible < float(info_json.get("cantidad")):
            return JsonResponse({"message": "Cantidad insuficiente", "status": 200}, status=200)
        product.cantidad = product.cantidad + state_product.cantidad_disponible
        product.save()

        product.cantidad = product.cantidad - float(info_json.get("cantidad"))
        state_product.cantidad_disponible = float(info_json.get("cantidad"))
        state_product.condiciones = info_json.get("condiciones")
        state_product.estado = info_json.get("estado")

        product.save()
        state_product.save()

        models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=request.user), producto=product, descripcion=f"Actualización de información de producto que está puesto a disposición, cantidad: {state_product.cantidad_disponible}, estado: {state_product.estado}")

        return JsonResponse({"message": "Información actualizada correctamente", "status": 201}, status=201)
    except (json.JSONDecodeError, ValueError, ValidationError, FieldError, ObjectDoesNotExist, IntegrityError, OperationalError, InternalError, models.Producto.DoesNotExist, models.Estados_de_producto.DoesNotExist) as e:
        print(e)
        return JsonResponse({"message": "Ocurrió un error al actualizar la información", "status": 500}, status=500)

# ?? Products
@require_http_methods(['PUT'])
@login_required(login_url="app:signin")
def update_tool(request: HttpRequest, id_tool: int) -> JsonResponse:
    '''
        Update tool
    '''
    try:
        r_json = json.loads(request.body.decode("utf-8"))
        producto = models.Producto.objects.get(pk=id_tool)
        cant_antes = producto.cantidad
        cant_des = float(r_json.get("cantidad"))
        name_tool = models.Producto.products.update_tool(models.Proveedor, id_tool, r_json)
        # models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Modificó producto {name_tool}")
        models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Modificó producto {name_tool}", producto=producto, cantidad_antes=cant_antes, cantidad_despues=cant_des)
        return JsonResponse({"message": "Herramienta actualizada correctamente", "status": 201}, status=201)
    except (models.Producto.DoesNotExist, json.JSONDecodeError, models.Proveedor.DoesNotExist, IntegrityError, OperationalError, InternalError, ValidationError, FieldError, ObjectDoesNotExist) as e:
        print(e)
        return JsonResponse({"message": "No se pudo modificar la herramienta correctamente"}, status=500)
        return JsonResponse({"message": f"Ocurrió un error en el sistema"}, status=500)

@require_http_methods(['PUT'])
@login_required(login_url="app:signin")
def update_item(request: HttpRequest, id_item: int) -> JsonResponse:
    '''
        Update item
    '''
    try:
        r_json = json.loads(request.body.decode("utf-8"))
        producto = models.Producto.objects.get(pk=id_item)
        # cant_antes = producto.cantidad
        # cant_des = float(r_json.get("cantidad"))
        name_item = models.Producto.products.update_item(models.Proveedor, id_item, r_json)
        models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Modificó producto {name_item}", producto=producto)
        return JsonResponse({"message": "Equipo actualizado correctamente", "status": 201}, status=201)
    except (models.Producto.DoesNotExist, json.JSONDecodeError) as e:
        print(e)
        return JsonResponse({"message": "No se pudo modificar el equipo correctamente"}, status=500)

# ?? Rents
@require_http_methods(['PUT'])
@login_required(login_url="app:signin")
def update_rent(request: HttpRequest, id_rent: int) -> JsonResponse:
    '''
        Update rent
    '''
    try:
        r_json= json.loads(request.body.decode("utf-8"))
        rent = models.Movimiento.objects.get(pk=id_rent)
        history = models.Historial()
        quantity_available = models.Estados_de_producto.objects.get(pk=rent.producto.pk)
        product = models.Producto.objects.get(pk=quantity_available.producto.pk)
        print(r_json)
        if float(r_json.get("cantidad")) > rent.cantidad + quantity_available.cantidad_disponible:
            return JsonResponse({"message": f"Cantidad insuficiente", "status": 200}, status=200)
        
        quantity_available.cantidad_disponible = quantity_available.cantidad_disponible + rent.cantidad
        quantity_available.save()

        quantity_available.cantidad_disponible = quantity_available.cantidad_disponible - float(r_json.get("cantidad"))
        quantity_available.save()

        rent.fecha_salida = r_json.get("fsalida") 
        rent.fecha_regreso = r_json.get("fregreso") 
        rent.cantidad = float(r_json.get("cantidad"))
        rent.save()
        history.movimiento = rent
        history.usuario = models.MyCustomUser.objects.get(username=request.user)
        history.producto = product
        history.descripcion = f'Actualización de renta de producto {product.descripcion}, cantidad actual: {rent.cantidad}'
        history.save()
        return JsonResponse({"message": f"Datos actualizados correctamente", "status": 201}, status=201)
    except(json.JSONDecodeError, IntegrityError, InternalError, OperationalError, InterruptedError, rent.DoesNotExist, models.MyCustomUser.DoesNotExist, product.DoesNotExist, quantity_available.DoesNotExist) as e:
        print(e)
        return JsonResponse({"message": f"No se pudo modificar la venta {id_rent}"}, status=500)

@require_http_methods(["PUT"])
@login_required
def return_rent(request: HttpRequest, id_rent: int) -> JsonResponse:
    '''
        Return rent when end date is reached
    '''
    try:
        history = models.Historial()
        product_rented = models.Movimiento.objects.get(pk=id_rent)
        product = models.Producto.objects.get(pk=product_rented.producto.pk)
        
        product.cantidad = product.cantidad + product_rented.cantidad
        product_rented.estado = 'Devuelto'
        product.save()
        product_rented.save()
        
        history.usuario = models.MyCustomUser.objects.get(username=request.user)
        history.producto = product
        history.descripcion = f'Renta de producto {product.descripcion} devuelta al inventario general.'
        history.save()
        return JsonResponse({"message": f"Producto {product.descripcion} rentado devuelto", "status": 200}, status=200)
    except (ValueError, ValidationError, FieldError, ObjectDoesNotExist, IntegrityError, OperationalError, InternalError, product_rented.DoesNotExist, product.DoesNotExist, models.MyCustomUser.DoesNotExist) as e:
        print(e)
        return JsonResponse({"message": f"Ocurrió un problema al devolver el producto", "status": 500}, status=500)

# ?? Sales
@require_http_methods(['PUT'])
@login_required(login_url="app:signin")
def update_sale(request: HttpRequest, id_sale: int) -> JsonResponse:
    '''
        Update sale
    '''
    try:
        r_json= json.loads(request.body.decode("utf-8"))
        sale = models.Movimiento.objects.get(pk=id_sale)
        history = models.Historial()
        quantity_available = models.Estados_de_producto.objects.get(pk=sale.producto.pk)
        product = models.Producto.objects.get(pk=quantity_available.producto.pk)

        if float(r_json.get("cantidad")) > sale.cantidad + quantity_available.cantidad_disponible:
            return JsonResponse({"message": f"Cantidad insuficiente", "status": 200}, status=200)
        
        quantity_available.cantidad_disponible = quantity_available.cantidad_disponible + sale.cantidad
        quantity_available.save()

        quantity_available.cantidad_disponible = quantity_available.cantidad_disponible - float(r_json.get("cantidad"))
        quantity_available.save()
        
        sale.fecha_salida = r_json.get("fsalida")
        sale.cantidad = float(r_json.get("cantidad"))
        sale.save()
        history.movimiento = sale
        history.usuario = models.MyCustomUser.objects.get(username=request.user)
        history.producto = product
        history.descripcion = f'Actualización de venta de herramienta {product.descripcion}, cantidad actual: {sale.cantidad}'
        history.save()
        return JsonResponse({"message": f"Datos actualizados correctamente", "status": 201}, status=201)
    except(models.Producto.DoesNotExist, json.JSONDecodeError, InternalError, IntegrityError, OperationalError, InterruptedError, sale.DoesNotExist, TypeError) as e:
        print(e)
        return JsonResponse({"message": f"No se pudo modificar la venta {id_sale}"}, status=500)


@require_http_methods(['PUT'])
@login_required
def cancel_sale(request: HttpRequest, id_sale: int) -> JsonResponse:
    try:
        user = models.MyCustomUser.objects.get(username=request.user)
        sale = models.Movimiento.objects.get(pk=id_sale)
        product = models.Producto.objects.get(pk=sale.producto.producto)
        history = models.Historial()
        
        if sale.estado == 'Cancelado':
            return JsonResponse({"message": "La venta ya está cancelada", "status": 200}, status=200)

        product.cantidad = product.cantidad + sale.cantidad
        sale.estado = 'Cancelado'
        
        product.save()
        sale.save()
        
        history.usuario = user
        history.producto = product
        history.descripcion = f"Venta de herramienta {product.descripcion} cancelada, cantidad actual en inventario: {product.cantidad}"
        history.save()
        
        return JsonResponse({"message": f"Venta de herramienta {product.descripcion} cancelada, cantidad regresada al inventario", "status": 201}, status=201)
    except (models.Movimiento.DoesNotExist, models.Producto.DoesNotExist) as e:
        print(e)
        return JsonResponse({"message": "Ocurrió un error al cancelar la venta", "status": 500}, status=500)

@require_http_methods(['PUT'])
@login_required
def cancel_rent(request: HttpRequest, id_sale: int) -> JsonResponse:
    try:
        user = models.MyCustomUser.objects.get(username=request.user)
        rent = models.Movimiento.objects.get(pk=id_sale)
        product = models.Producto.objects.get(pk=rent.producto.producto)
        history = models.Historial()

        if rent.estado == 'Cancelado':
            return JsonResponse({"message": "La venta ya está cancelada", "status": 200}, status=200)
        
        history.usuario = user
        history.producto = product
        product.cantidad = product.cantidad + rent.cantidad
        rent.estado = 'Cancelado'
        if product.categoria == 'HERRAMIENTA':
            product.save()
            rent.save()
            history.movimiento = rent
            history.descripcion = f"Renta de herramienta {product.descripcion} cancelada, cantidad actual en inventario: {product.cantidad}"
            history.save()
            
            return JsonResponse({"message": f"Renta de herramienta {product.descripcion} cancelada, cantidad regresada al inventario", "status": 201}, status=201)
        product.save()
        rent.save()
        history.movimiento = rent
        history.descripcion = f"Renta de equipo {product.descripcion} cancelada, cantidad actual en inventario: {product.cantidad}"
        history.save()
        return JsonResponse({"message": f"Renta de herramienta {product.descripcion} cancelada, cantidad regresada al inventario", "status": 201}, status=201)
        
    except (models.Movimiento.DoesNotExist, models.Producto.DoesNotExist) as e:
        print(e)
        return JsonResponse({"message": "Ocurrió un error al cancelar la venta", "status": 500}, status=500)