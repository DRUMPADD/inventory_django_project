from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError, FieldError, ObjectDoesNotExist
from django.db import IntegrityError, OperationalError, InternalError
from .. import models
import json

# ?? Products
@require_POST
@login_required(login_url="app:signin")
def delete_product(request: HttpRequest, id_product: int) -> JsonResponse:
    '''
        Deactivate product
    '''
    try:
        category = models.Producto.objects.get(pk=id_product)
        state_product = models.Producto.products.delete_product(id_product)
        if not state_product:
            models.Historial.objects.create(usuario=models.MyCustomUser.objects.get(username=str(request.user)), descripcion=f"Eliminó producto {id_product}", producto=category)
        if category.categoria == 'EQUIPO':
            return JsonResponse({"message": "Equipo eliminado", "status": 204}, status=204)
        return JsonResponse({"message": "Herramienta especial eliminada", "status": 204}, status=204)
    except (models.Producto.DoesNotExist, json.JSONDecodeError, ValidationError, FieldError, ObjectDoesNotExist, IntegrityError, OperationalError, InternalError) as e:
        print(e)
        return JsonResponse({"message": "Ocurrió un error al eliminar el producto", "status": 500}, status=500)
