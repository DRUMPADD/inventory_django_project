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
        state_product = models.Producto.products.delete_product(id_product)
        if not state_product:
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Eliminó producto {id_product}")
        return redirect("app:tools")
    except (models.Producto.DoesNotExist, json.JSONDecodeError) as e:
        print(e)
        return redirect("app:tools")