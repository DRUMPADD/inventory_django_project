from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import exceptions
from . import models
# Create your views here.
@require_http_methods(['GET', 'POST'])
def login_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.user.is_authenticated:
        return redirect("app:tools")
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "app:tools")
            return redirect(next_url)
        else:
            messages.warning(request, "El usuario o contraseña es incorrecto")
    return render(request, "accounts/login.html")

@require_http_methods(['GET', 'POST'])
def signup_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.user.is_authenticated:
        return redirect("app:tools")
    if request.method == 'POST':
        username = request.POST.get("username")
        name = request.POST.get("name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        models.MyCustomUser.objects.create_user(username=username, name_user=name, middle_name=middle_name, last_name=last_name, password=password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("app:tools")
        else:
            print(user)
            messages.warning(request, "El usuario o contraseña es incorrecto")
    # if request.method == 'POST':
    #     if models.MyCustomUser.objects.filter(username=request.POST.get("username")):
    #         messages.warning(request, "El usuario ya existe", "", fail_silently=True)
    return render(request, "accounts/signup.html", {})

@require_GET
@login_required(login_url="app:signin")
def index(request: HttpRequest) -> HttpResponse:
    tools = models.Producto.objects.filter(categoria="HERRAMIENTA", disponible=True)
    suppliers = models.Proveedor.objects.all()
    products_available = models.Producto.products.filter_products_available(models.Movimiento)
    products_sold = models.Movimiento.movements.filter_products_sold(category='HERRAMIENTA')
    products_rented = models.Movimiento.movements.filter_products_rented(category='HERRAMIENTA')
    codes = models.Producto.products.get_codes('HERRAMIENTA')
    tools_filtered_rented = models.Movimiento.movements.filter_products_by_name_size_rented("HERRAMIENTA")
    tools_filtered = models.Producto.products.filter_products_by_name_size(models.Estados_de_producto, "HERRAMIENTA")
    print(tools_filtered_rented)
    context: dict = {}
    context["tools"] = tools
    context["codes"] = codes
    context["suppliers"] = suppliers
    context["products_available"] = products_available
    context["products_sold"] = products_sold
    context["products_filtered"] = tools_filtered
    context["products_rented"] = products_rented
    context["products_filtered_rented"] = tools_filtered_rented
    return render(request, "index.html", context)

@require_GET
@login_required(login_url="app:signin")
def items(request: HttpRequest) -> HttpResponse:
    context: dict = {}
    suppliers = models.Proveedor.objects.all()
    items = models.Producto.objects.filter(categoria="EQUIPO", disponible=True)
    items_filtered = models.Producto.products.filter_products_by_name_size(models.Movimiento, "EQUIPO")
    items_filtered_rented = models.Movimiento.movements.filter_products_by_name_size_rented("EQUIPO")
    codes = models.Producto.products.get_codes('EQUIPO')
    context["items"] = items
    context["codes"] = codes
    context["suppliers"] = suppliers
    context["items_filtered"] = items_filtered
    context["items_filtered_rented"] = items_filtered_rented
    return render(request, "items.html", context)

@login_required(login_url="app:signin")
def tool_view(request: HttpRequest, id_tool: int) -> HttpResponse:
    context = {}
    tool = models.Producto.products.get_tool_info(id_tool)
    # status = models.Estados.objects.all()
    # movement_types = models.Tipos_movimiento.objects.all()
    tools_in_use = models.Estados_de_producto.objects.filter(producto__pk=id_tool).values('pk', 'producto__descripcion', 'producto__pk', 'cantidad_disponible', 'estado', 'condiciones')
    suppliers = models.Proveedor.objects.all()
    context["tool"] = tool[0]
    context["suppliers"] = suppliers
    try:
        # print(models.Estados_de_producto.objects.get(producto=id_tool).pk)
        context["tool_using"] = models.Estados_de_producto.objects.get(producto=id_tool)
    except models.Estados_de_producto.DoesNotExist:
        context["tool_using"] = {}
        print("No existe")
    # context["status"] = status
    context["items_use"] = tools_in_use
    # context["movement_types"] = movement_types
    return render(request, "tool.html", context)

@login_required(login_url="app:signin")
def item_view(request: HttpRequest, id_item: int):
    context = {}
    item = models.Producto.products.get_item_info(id_item)
    # movement_types = models.Tipos_movimiento.objects.all()
    # status = models.Estados.objects.all()
    # items_in_use = models.Estados_de_producto.objects.filter(producto__pk=id_item).values('pk', 'producto__descripcion', 'producto__pk', 'cantidad_disponible', 'estado', 'condiciones')
    items_use = models.Movimiento.objects.filter(producto__producto__pk=id_item, estado='En uso').values('pk', 'producto__producto__descripcion', 'producto__pk', 'cantidad', 'estado', 'producto__condiciones', 'producto__estado')
    print(items_use)
    suppliers = models.Proveedor.objects.all()
    context["suppliers"] = suppliers
    context["item"] = item[0]
    # context["status"] = status
    # context["movement_types"] = movement_types
    context["items_use"] = items_use
    return render(request, "item.html", context)

@login_required
def movement_view(request: HttpRequest, option: int, id_mov: int) -> HttpResponse:
    context: dict = {}
    if option == 1:
        product_info = models.Movimiento.movements.get_sale_info(id_mov)
        is_sale = True
    else:
        product_info = models.Movimiento.movements.get_rent_info(id_mov)
        is_sale = False
    products = models.Producto.objects.all().values("pk", "descripcion")
    context["products"] = products
    context["item"] = product_info[0]
    context["option"] = is_sale
    return render(request, "sale_rent.html", context)

@require_GET
@login_required(login_url="app:signin")
def sales(request: HttpRequest) -> HttpResponse:
    context: dict = {}
    sales_ = models.Movimiento.movements.get_all_products_sold()
    context["sales"] = sales_
    return render(request, "sales.html", context)

@require_GET
@login_required(login_url="app:signin")
def rents(request: HttpRequest) -> HttpResponse:
    context: dict = {}
    rents_ = models.Movimiento.movements.get_all_products_rented()
    context["rents"] = rents_
    return render(request, "rents.html", context)
    
@require_GET
@login_required(login_url="app:signin")
def history(request: HttpRequest) -> HttpResponse:
    context: dict = {}
    history = models.Historial.get_history(models.Historial)
    context["history"] = history
    return render(request, "history.html", context)
    
def logout_(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("app:signin")

def custom_error_404(request: HttpRequest, exception: exceptions) -> HttpResponse:
    return render(request, "errors/error404.html")

def custom_error_500(request: HttpRequest) -> HttpResponse:
    return render(request, "errors/error500.html")