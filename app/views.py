from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from . import models
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True)
def login_view(request: HttpRequest):
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

@cache_control(no_cache=True, must_revalidate=True)
def signup_view(request: HttpRequest):
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

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url="app:signin")
def index(request: HttpRequest):
    print(request.user)
    tools = models.Producto.objects.filter(categoria="HERRAMIENTA", disponible=True)
    suppliers = models.Proveedor.objects.all()
    products_available = models.Producto.products.filter_products_available(models.Venta, models.Renta)
    products_sold = models.Venta.sales.filter_products_sold()
    products_rented = models.Renta.rents.filter_products_rented()
    codes = models.Producto.products.get_codes('HERRAMIENTA')
    tools_filtered_rented = models.Renta.rents.filter_products_by_name_size_rented("HERRAMIENTA")
    tools_filtered = models.Producto.products.filter_products_by_name_size(models.Renta, models.Venta, "HERRAMIENTA")
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

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url="app:signin")
def items(request: HttpRequest):
    context: dict = {}
    suppliers = models.Proveedor.objects.all()
    items = models.Producto.objects.filter(categoria="EQUIPO", disponible=True)
    items_filtered = models.Producto.products.filter_products_by_name_size(models.Renta, models.Venta, "EQUIPO")
    items_filtered_rented = models.Renta.rents.filter_products_by_name_size_rented("EQUIPO")
    codes = models.Producto.products.get_codes('EQUIPO')
    context["items"] = items
    context["codes"] = codes
    context["suppliers"] = suppliers
    context["items_filtered"] = items_filtered
    context["items_filtered_rented"] = items_filtered_rented
    return render(request, "items.html", context)

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url="app:signin")
def sales(request: HttpRequest):
    context: dict = {}
    sales_ = models.Venta.sales.get_all_products_sold()
    context["sales"] = sales_
    return render(request, "sales.html", context)

@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url="app:signin")
def rents(request: HttpRequest):
    context: dict = {}
    rents_ = models.Renta.rents.get_all_products_rented()
    context["rents"] = rents_
    return render(request, "rents.html", context)
    
@cache_control(no_cache=True, must_revalidate=True)
@login_required(login_url="app:signin")
def history(request: HttpRequest):
    context: dict = {}
    history = models.Historial.get_history(models.Historial)
    context["history"] = history
    return render(request, "history.html", context)
    
def logout_(request: HttpRequest):
    logout(request)
    return redirect("app:signin")