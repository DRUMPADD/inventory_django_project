from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views, actions

app_name = 'app'

urlpatterns = [
    path('', views.login_view, name="signin"),
    path('registro', views.signup_view, name="signup"),
    path('cerrar_sesion', views.logout_, name="signout"),
    path('herramientas', views.index, name="tools"),
    path('equipos', views.items, name="items"),
    path('ventas', views.sales, name="sales"),
    path('rentas', views.rents, name="rents"),
    path('historial', views.history, name="history"),

    path(r'herramientas/<id_tool>', actions.tool_view, name="tool"),
    path(r'equipos/<id_item>', actions.item_view, name="item"),
    path(r'movimiento/<int:option>/<int:id_mov>', actions.movement_view, name="movement"),

    path('agregar-proveedor/<path_>', actions.add_supplier, name="add_supplier"),
    path('agregar_herramienta', actions.create_tool, name="add_tool"),
    path('modificar_herramienta/<int:id_tool>', actions.update_tool, name="update_tool"),
    path('agregar_equipo', actions.create_item, name="add_item"),
    path('modificar_equipo/<int:id_item>', actions.update_item, name="update_item"),
    path('modificar_venta/<int:id_sale>', actions.update_sale, name="update_sale"),
    path('modificar_renta/<int:id_rent>', actions.update_rent, name="update_rent"),
    path('eliminar_producto/<id_product>', actions.delete_product, name="delete_product"),

]