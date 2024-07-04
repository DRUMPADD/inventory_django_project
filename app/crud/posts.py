import json.tool
from django.shortcuts import redirect
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError, FieldError, ObjectDoesNotExist
from django.db import IntegrityError, OperationalError, InternalError
from .. import models
import json

# ?? Providers
@require_POST
@login_required(login_url="app:signin")
def add_supplier(request: HttpRequest, path_: str) -> HttpResponseRedirect:
    '''
        Add new supplier
    '''
    folio = request.POST.get("folio")
    nombre = request.POST.get("nombre")
    try:
        models.Proveedor.objects.create(folio=folio, nombre=nombre)
        return redirect(f'/{path_}')
    except (models.Proveedor.DoesNotExist, ValueError, KeyError) as e:
        print(e)
        return redirect(f'/{path_}')

# ?? Products
@require_POST
@login_required(login_url="app:signin")
def create_product(request: HttpRequest) -> JsonResponse:
    '''
        Register new product
    '''
    try:
        r_json = json.loads(request.body.decode("utf-8"))
        print(str(request.user))
        user = models.MyCustomUser.objects.get(username=request.user)
        new_product = models.Producto.products.create_product(models.Proveedor, data=r_json)
        models.Historial.objects.create(usuario=user, producto=new_product, descripcion=f"Nuevo producto: {r_json.get("producto")} agregado")
        if r_json.get("categoria") == 'HERRAMIENTA':
            return JsonResponse({"message": f"Herramienta especial {r_json.get("producto")} agregada", "status": 201}, status=201)
        return JsonResponse({"message": f"Equipo {r_json.get("producto")} agregado", "status": 201}, status=201)
    except (json.JSONDecodeError, models.Producto.DoesNotExist, models.Proveedor.DoesNotExist, ValueError, ValidationError, FieldError, ObjectDoesNotExist) as e:
        print(e)
        return JsonResponse({"message": "No se pudo agregar el producto correctamente"}, status=500)

# ?? States of product
@require_POST
@login_required
def dispose_product(request: HttpRequest, id: int) -> JsonResponse:
    '''
        Dispose product before to make use of itself
    '''
    try:
        r_json = json.loads(request.body.decode('utf-8'))

        user = models.MyCustomUser.objects.get(username=request.user)
        product = models.Producto.objects.get(pk=id)
        try:
            state_product = models.Estados_de_producto.objects.get(producto=id)
            if product.cantidad + state_product.cantidad_disponible < float(r_json.get("cantidad")):
                return JsonResponse({"message": "Cantidad disponible insuficiente", "status": 200}, status=200)
            
            product.cantidad = product.cantidad - float(r_json.get("cantidad"))
            product.save()

            state_product.cantidad_disponible = state_product.cantidad_disponible + float(r_json.get("cantidad"))
            state_product.condiciones = r_json.get("condiciones")
            state_product.estado = r_json.get("estado")
            state_product.save()
            product.save()
            history = models.Historial()
            history.descripcion = f"Actualización de información de producto que está puesto a disposición, cantidad: {state_product.cantidad_disponible}, estado: {state_product.estado}"
            history.producto = product
            history.usuario = user
            history.save()
            if product.categoria == 'HERRAMIENTA':
                return JsonResponse({"message": "Disposición de herramienta: " + product.descripcion + " registrada", "status": 201}, status=201)
            return JsonResponse({"message": "Disposición de equipo: " + product.descripcion + " registrado", "status": 201}, status=201)
        except (models.Estados_de_producto.DoesNotExist) as e:
            if product.cantidad < float(r_json.get("cantidad")):
                return JsonResponse({"message": "Cantidad disponible insuficiente", "status": 200}, status=200)

            models.Estados_de_producto.uses.dispose_product(product=product, info=r_json)
            product.cantidad = product.cantidad - float(r_json.get("cantidad"))
            history = models.Historial()
            history.descripcion = 'Disposición de producto ' + product.descripcion + ', cantidad: ' + r_json.get("cantidad")
            history.producto = product
            history.usuario = user
            product.save()
            history.save()
            if product.categoria == 'HERRAMIENTA':
                return JsonResponse({"message": "Disposición de herramienta: " + product.descripcion + " registrada", "status": 201}, status=201)
            return JsonResponse({"message": "Disposición de equipo: " + product.descripcion + " registrado", "status": 201}, status=201)
    except (json.JSONDecodeError, IntegrityError, InternalError, OperationalError, ValidationError, FieldError, ObjectDoesNotExist, models.MyCustomUser.DoesNotExist, models.Producto.DoesNotExist) as e:
        print(e)
        return JsonResponse({"message": "Ocurrió un error al usar el producto", "status": 500}, status=500)

# @require_POST
# @login_required
# def register_transaction(request: HttpRequest, id: int) -> JsonResponse:
#     '''
#         Register transaction when product's state is ready to rent, sale or use
#     '''
#     try:
#         req_json = json.loads(request.body.decode('utf-8'))
#         product = models.Producto.objects.get(pk=id)
#         status = models.Estados.objects.get(pk=int(req_json.get("sl_status")))
#         types_mov = models.Tipos_movimiento.objects.get(pk=int(req_json.get("tipo_mov")))
#         if product.cantidad < float(req_json.get("cantidad")):
#             return JsonResponse(data={"message": "No hay suficiente equipo disponible", "status": 204}, status=204)
#         user = models.MyCustomUser.objects.get(username=request.user)
#         if req_json.get("tipo_mov") != '2':
#             models.Movimientos.movements.create_rent_or_sale(product=product, info=req_json, user=user, status=status, types_mov=types_mov)
#         else:
#             models.Movimientos.movements.create_use_of_product(info=req_json, product=product, user=user, types_mov=types_mov, status=status)
#         product.cantidad = product.cantidad - float(req_json.get("cantidad"))
#         product.save()
#         history = models.Historial()
#         history.producto = product
#         history.usuario = user
#         history.cantidad_antes = product.cantidad + float(req_json.get("cantidad"))
#         history.cantidad_despues = product.cantidad
#         if req_json.get("tipo_mov") == '1': history.descripcion = f"Producto {product.descripcion} rentado, cantidad rentada: {float(req_json.get("cantidad"))}, estado: {status.nombre}"
#         elif req_json.get("tipo_mov") == '2': history.descripcion = f"Producto {product.descripcion} en uso, cantidad en uso: {float(req_json.get("cantidad"))}, estado: {status.nombre}"
#         else: history.descripcion = f"Producto {product.descripcion} vendido, cantidad vendida: {float(req_json.get("cantidad"))}, estado: {status.nombre}"
#         history.save()
#         if req_json.get("tipo_mov") == '1':
#             return JsonResponse({"message": f"Producto fue registrado como renta", "status": 201}, status=201)
#         if req_json.get("tipo_mov") == '2':
#             return JsonResponse({"message": f"Producto registrado en uso", "status": 201}, status=201)
#         else:
#             return JsonResponse({"message": f"Producto fue registrado como venta", "status": 201}, status=201)
#     except(models.Producto.DoesNotExist, models.MyCustomUser.DoesNotExist, json.JSONDecodeError, ValueError, ValidationError, FieldError, ObjectDoesNotExist, IntegrityError, OperationalError, InternalError) as e:
#         print(e)
# ?? Movements: sales, rents, uses
@require_POST
@login_required
def register_transaction_tool(request: HttpRequest, id: int) -> JsonResponse:
    '''
        Register transaction when product's state is ready to rent, sale or use
    '''
    try:
        req_json = json.loads(request.body.decode('utf-8'))
        mov_type = str(req_json.get("mov_type"))
        state_product = models.Estados_de_producto.objects.get(pk=id)
        product = models.Producto.objects.get(pk=state_product.producto.pk)
        movement = models.Movimiento()
        history = models.Historial()
        print(product)
        if state_product.cantidad_disponible < float(req_json.get("cantidad")):
            return JsonResponse({"message": "Cantidad disponible insuficiente", "status": 200}, status=200)
        if mov_type == 'VENTA':
            print(req_json)
            movement.producto = state_product
            movement.tipo_movimiento = mov_type.capitalize()
            movement.cantidad = float(req_json.get("cantidad"))
            movement.estado = "Vendido"
            movement.fecha_salida = req_json.get("fsalida")
        elif mov_type == 'RENTA':
            print(req_json)
            movement.producto = state_product
            movement.tipo_movimiento = mov_type.capitalize()
            movement.cantidad = float(req_json.get("cantidad"))
            movement.estado = "Rentado"
            movement.fecha_salida = req_json.get("fsalida")
            movement.fecha_regreso = req_json.get("fregreso")
        else:
            movement.producto = state_product
            movement.tipo_movimiento=mov_type.capitalize()
            movement.cantidad=float(req_json.get("cantidad"))
            movement.estado="En uso"
        state_product.cantidad_disponible = state_product.cantidad_disponible - float(req_json.get("cantidad"))
        movement.save()
        if movement.pk:
            state_product.save()
            history.usuario = models.MyCustomUser.objects.get(username=request.user)
            history.descripcion = f"Herramienta registrada como {mov_type.capitalize()}"
            history.movimiento = movement
            history.producto = product
            history.save()
        else: raise ObjectDoesNotExist("No se ha podido guardar el dato")
        if product.categoria == 'HERRAMIENTA':
            return JsonResponse({"message": f"Herramienta registrada como {mov_type.capitalize()}", "status": 201}, status=201)
        return JsonResponse({"message": f"Equipo registrado como {mov_type.capitalize()} ", "status": 201}, status=201)
    except(models.Producto.DoesNotExist, models.MyCustomUser.DoesNotExist, json.JSONDecodeError, ValueError, ValidationError, FieldError, ObjectDoesNotExist, IntegrityError, OperationalError, InternalError) as e:
        print(e)
        return JsonResponse({"message": f"Ocurrió un error al registrar el movimiento", "status": 500}, status=500)

@require_POST
@login_required
def register_transaction_item(request: HttpRequest, id: int) -> JsonResponse:
    '''
        Register transaction when product's state is ready to rent, sale or use
    '''
    try:
        req_json = json.loads(request.body.decode('utf-8'))
        mov_type = str(req_json.get("tipo_mov"))
        product = models.Producto.objects.get(pk=id)
        state_product = models.Estados_de_producto(
            producto=product,
            cantidad_disponible=float(req_json.get("cantidad")),
            condiciones=req_json.get("condicion"),
            estado=req_json.get("sl_status"),
        )
        movement = models.Movimiento()
        history = models.Historial()
        print("Producto ",product)
        if product.cantidad < float(req_json.get("cantidad")):
            return JsonResponse({"message": "Cantidad disponible insuficiente", "status": 200}, status=200)
        product.cantidad = product.cantidad - float(req_json.get("cantidad"))
        state_product.save()
        product.save()
        print("Cantidad actual:", product.cantidad)
        if mov_type == 'RENTA':
            print(req_json)
            movement.producto = state_product
            movement.tipo_movimiento = mov_type.capitalize()
            movement.cantidad = float(req_json.get("cantidad"))
            movement.estado = "Rentado"
            movement.fecha_salida = req_json.get("fsalida")
            movement.fecha_regreso = req_json.get("fregreso")
        else:
            movement.producto = state_product
            movement.tipo_movimiento = mov_type.capitalize()
            movement.cantidad = float(req_json.get("cantidad"))
            movement.estado = "En uso"
        movement.save()
        if movement.pk:
            state_product.save()
            history.usuario = models.MyCustomUser.objects.get(username=request.user)
            history.descripcion = f"Equipo registrado como {mov_type.capitalize()}"
            history.movimiento = movement
            history.producto = product
            history.save()
        else: raise ObjectDoesNotExist("No se ha podido guardar el dato")
        return JsonResponse({"message": f"Equipo registrado como {mov_type.capitalize()} ", "status": 201}, status=201)
    except(models.Producto.DoesNotExist, models.MyCustomUser.DoesNotExist, json.JSONDecodeError, ValueError, ValidationError, FieldError, ObjectDoesNotExist, IntegrityError, OperationalError, InternalError) as e:
        print(e)
        return JsonResponse({"message": f"Ocurrió un error al registrar el movimiento", "status": 500}, status=500)

# @require_POST
# @login_required(login_url="app:signin")
# def create_use_of_product(request: HttpRequest, id: int):
#     try:
#         info_product = models.Producto.objects.get(pk=id)
#         user = models.MyCustomUser.objects.get(username=request.user)
#         info = json.loads(request.body.decode("utf-8"))
#         # product = models.Movimientos()
#         # product.producto = info_product
#         # product.cantidad = float(info.get("cantidad"))
#         # product.tipo_movimiento = info.get("tipo_mov")
#         # product.estado = info.get("sl_status")
#         # product.condicion = info.get("condicion")
#         # product.usuario = user
#         # product.fecha_regreso = info.get("fecha_regreso")
#         # product.fecha_salida = info.get("fecha_salida")
#         models.Movimientos.movements.create_use_of_product(info=info, product=info_product, user=user, types_mov_model=models.Tipos_movimiento, status_model=models.Estados)

#         if info_product.cantidad < float(info.get("cantidad")):
#             return JsonResponse(data={"message": "No hay suficiente equipo disponible", "status": 204}, status=204)
#         info_product.cantidad = info_product.cantidad - float(info.get("cantidad"))
#         info_product.save()

#         if info.get("tipo_mov") == '2':
#             models.Historial.objects.create(usuario=user, producto=info_product, descripcion=f"Salida de producto en uso {info_product.descripcion}, cantidad actual: {info_product.cantidad}", cantidad_antes=info_product.cantidad+float(info.get("cantidad")), cantidad_despues=info_product.cantidad)
#         elif info.get("tipo_mov") == '1':
#             models.Historial.objects.create(usuario=user, producto=info_product, descripcion=f"Renta de producto {info_product.descripcion}, cantidad actual: {info_product.cantidad}", cantidad_antes=info_product.cantidad+float(info.get("cantidad")), cantidad_despues=info_product.cantidad)
#         else:
#             models.Historial.objects.create(usuario=user, producto=info_product, descripcion=f"Venta de producto {info_product.descripcion}, cantidad actual: {info_product.cantidad}", cantidad_antes=info_product.cantidad+float(info.get("cantidad")), cantidad_despues=info_product.cantidad)
#         return JsonResponse({"message": "Equipo registrado en uso", "status": 201}, status=201)
#     except (json.JSONDecodeError):
#         return JsonResponse({"message": "Error en el sistema", "status": 500}, status=500)