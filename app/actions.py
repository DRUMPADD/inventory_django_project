from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.core.exceptions import ValidationError, FieldError, ObjectDoesNotExist
from . import models
import json

@require_POST
@login_required(login_url="app:signin")
def add_supplier(request: HttpRequest, path_: str):
    folio = request.POST.get("folio")
    nombre = request.POST.get("nombre")
    try:
        models.Proveedor.objects.create(folio=folio, nombre=nombre)
        return redirect(f'/{path_}')
    except (models.Proveedor.DoesNotExist, ValueError, KeyError) as e:
        print(e)
        return redirect(f'/{path_}')

@require_POST
@login_required(login_url="app:signin")
def create_tool(request: HttpRequest):
    try:
        r_json = json.loads(request.body.decode("utf-8"))
        print(str(request.user))
        user = models.MyCustomUser.objects.get(username=request.user)
        new_product = models.Producto.products.create_tool(models.Proveedor, data=r_json)
        if r_json.get("sl_opcion") == "1":
            new_sale = models.Venta.sales.register_sale(models.Producto, new_product, r_json)
            models.Historial.objects.create(usuario=user, descripcion="Registró nuevo producto en venta", venta=models.Venta.objects.get(pk=new_sale))
        if r_json.get("sl_opcion") == "2":
            new_rent = models.Renta.rents.register_rent(models.Producto, new_product, r_json)
            models.Historial.objects.create(usuario=user, descripcion="Registró nuevo producto en renta", renta=models.Renta.objects.get(pk=new_rent))
        if r_json.get("sl_opcion") == "3" or r_json.get("sl_opcion") == "4":
            models.Historial.objects.create(usuario=user, descripcion=f"Registró nuevo producto: {r_json.get('herramienta')}")
        return JsonResponse({"message": "Herramienta especial agregada"}, status=201)
    except (json.JSONDecodeError, models.Producto.DoesNotExist, models.Proveedor.DoesNotExist, ValueError, ValidationError, FieldError, ObjectDoesNotExist) as e:
        print(e)
        return JsonResponse({"message": "No se pudo agregar la herramienta correctamente"}, status=500)
@require_POST
@login_required(login_url="app:signin")
def create_item(request: HttpRequest):
    try:
        r_json = json.loads(request.body.decode("utf-8"))
        new_product = models.Producto.products.create_item(models.Proveedor, data=r_json)
        if r_json.get("sl_opcion") == "1":
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Registró nuevo producto: {r_json.get('articulo')}")
        if r_json.get("sl_opcion") == "2":
            new_rent = models.Renta.rents.register_rent(models.Producto, new_product, r_json)
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion="Registró nuevo producto en renta", renta=models.Renta.objects.get(pk=new_rent))
        return JsonResponse({"message": "Equipo agregado correctamente"}, status=201)
    except (json.JSONDecodeError, models.Producto.DoesNotExist, models.Proveedor.DoesNotExist, ValidationError, FieldError, ObjectDoesNotExist, ValueError) as e:
        print(e)
        return JsonResponse({"message": "No se pudo agregar el equipo correctamente"}, status=500)

@require_http_methods(['PUT'])
@login_required(login_url="app:signin")
def update_tool(request: HttpRequest, id_tool: int):
    try:
        r_json = json.loads(request.body.decode("utf-8"))
        name_tool = models.Producto.products.update_tool(models.Proveedor, id_tool, r_json)
        if name_tool != "":
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Modificó producto {name_tool}")
        return JsonResponse({"message": "Herramienta actualizada correctamente"}, status=201)
    except (models.Producto.DoesNotExist, json.JSONDecodeError, models.Proveedor.DoesNotExist) as e:
        print(e)
        return JsonResponse({"message": "No se pudo modificar la herramienta correctamente"}, status=500)

@require_http_methods(['PUT'])
@login_required(login_url="app:signin")
def update_item(request: HttpRequest, id_item: int):
    try:
        r_json = json.loads(request.body.decode("utf-8"))
        name_item = models.Producto.products.update_item(models.Proveedor, id_item, r_json)
        if name_item != "":
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Modificó producto {name_item}")
        return JsonResponse({"message": "Equipo actualizado correctamente"}, status=201)
    except (models.Producto.DoesNotExist, json.JSONDecodeError) as e:
        print(e)
        return JsonResponse({"message": "No se pudo modificar el equipo correctamente"}, status=500)

@require_http_methods(['PUT'])
@login_required(login_url="app:signin")
def update_sale(request: HttpRequest, id_sale: int):
    try:
        r_json= json.loads(request.body.decode("utf-8"))
        models.Venta.sales.update_sale(models.Producto, id_sale, r_json)
        return JsonResponse({"message": f"Datos actualizados correctamente"}, status=201)
    except(models.Producto.DoesNotExist, models.Venta.DoesNotExist, json.JSONDecodeError) as e:
        print(e)
        return JsonResponse({"message": f"No se pudo modificar la venta {id_sale}"}, status=500)

@require_http_methods(['PUT'])
@login_required(login_url="app:signin")
def update_rent(request: HttpRequest, id_rent: int):
    try:
        r_json= json.loads(request.body.decode("utf-8"))
        models.Renta.rents.update_rent(models.Producto, id_rent, r_json)
        return JsonResponse({"message": f"Datos actualizados correctamente"}, status=201)
    except(models.Producto.DoesNotExist, models.Venta.DoesNotExist, json.JSONDecodeError) as e:
        print(e)
        return JsonResponse({"message": f"No se pudo modificar la venta {id_rent}"}, status=500)

@require_http_methods(['GET', 'DELETE'])
@login_required(login_url="app:signin")
def delete_product(request: HttpRequest, id_product: int):
    try:
        category = models.Producto.objects.get(pk=id_product)
        state_product = models.Producto.products.delete_product(id_product)
        if not state_product:
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Eliminó producto {id_product}")
        if category.categoria == 'EQUIPO':
            return redirect("app:items")
        return redirect("app:tools")
    except (models.Producto.DoesNotExist, json.JSONDecodeError) as e:
        print(e)
        return redirect("app:tools")

@require_http_methods(['POST'])
@login_required(login_url="app:signin")
def create_use_of_product(request: HttpRequest, id: int):
    try:
        info_product = models.Producto.objects.get(pk=id)
        info = json.loads(request.body.decode("utf-8"))
        product = models.Producto_uso()
        product.producto = info_product
        product.cantidad_uso = float(info.get("cantidad_uso"))
        product.estado = info.get("sl_status")
        product.condicion = info.get("condicion")
        if info_product.cantidad < float(info.get("cantidad_uso")):
            return JsonResponse(data={"message": "No hay suficiente equipo disponible", "status": 204}, status=204)
        info_product.cantidad = info_product.cantidad - float(info.get("cantidad_uso"))
        info_product.save()
        product.save()
        models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Salida de producto en uso {info_product.descripcion}, cantidad actual: {info_product.cantidad}")
        return JsonResponse({"message": "Equipo registrado en uso", "status": 201}, status=201)
    except (json.JSONDecodeError):
        return JsonResponse({"message": "Error en el sistema", "status": 500}, status=500)

@require_http_methods(["PUT"])
@login_required(login_url="app:signin")
def update_use_of_product(request: HttpRequest, id_product: int, id_product_use: int):
    try:
        product = models.Producto.objects.get(pk=id_product)
        product_use = models.Producto_uso.objects.get(pk=id_product_use)
        info = json.loads(request.body.decode("utf-8"))
        product_use.estado = info.get("sl_status")
        product_use.condicion = info.get("condicion")
        # if float(info.get("cantidad_uso")) != product_use.cantidad_uso or info.get("sl_status") != 'Listo':
        if float(info.get("cantidad_uso")) > product_use.cantidad_uso:
            if float(info.get("cantidad_uso")) - product_use.cantidad_uso < product.cantidad:
                product.cantidad = (product.cantidad + product_use.cantidad_uso) - float(info.get("cantidad_uso"))
                product_use.cantidad_uso = float(info.get("cantidad_uso"))
            else:
                product_use.save()
                return JsonResponse({"message": "No hay suficiente equipo disponible", "status": 204}, status=204)
        if float(info.get("cantidad_uso")) < product_use.cantidad_uso:
            product.cantidad = (product_use.cantidad_uso - float(info.get("cantidad_uso"))) + product.cantidad
            product_use.cantidad_uso = float(info.get("cantidad_uso"))
        if float(info.get("cantidad_uso")) == product_use.cantidad_uso and info.get("sl_status") == 'Listo':
            product.cantidad = product.cantidad + float(info.get("cantidad_uso"))
        if info.get("sl_status") == 'Listo':
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Entrada de producto {product.descripcion} que estuvo en uso, cantidad actual: {product.cantidad}")
            product_use.save()
            product.save()
            print(product.cantidad)
        else:
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Actualización de producto {product.descripcion} en uso, cantidad actual: {product.cantidad}")
            product_use.save()
            print(product_use)
            product.save()
        return JsonResponse({"message": "Actualización de equipo en uso", "status": 200}, status=200)
    except (json.JSONDecodeError):
        return JsonResponse({"message": "Error en el sistema", "status": 500}, status=500)