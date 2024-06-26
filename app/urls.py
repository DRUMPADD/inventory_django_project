from django.urls import path, re_path
from django.views.generic.base import RedirectView
from . import views, actions

app_name = 'app'

urlpatterns = [
    path('', views.login_view, name="signin"),
    path('registrar_usuario', views.signup_view, name="signup"),
    path('cerrar_sesion', views.logout_, name="signout"),
    path('herramientas', views.index, name="tools"),
    path('equipos', views.items, name="items"),
    path('ventas', views.sales, name="sales"),
    path('rentas', views.rents, name="rents"),
    path('historial', views.history, name="history"),

    path(r'herramientas/<id_tool>', views.tool_view, name="tool"),
    path(r'equipos/<id_item>', views.item_view, name="item"),
    path(r'movimiento/<int:option>/<int:id_mov>', views.movement_view, name="movement"),

    path('agregar-proveedor/<path_>', actions.add_supplier, name="add_supplier"),
    path('agregar_herramienta', actions.create_tool, name="add_tool"),
    path('modificar_herramienta/<int:id_tool>', actions.update_tool, name="update_tool"),
    path('agregar_equipo', actions.create_item, name="add_item"),
    path('agregar_equipo_uso/<int:id>', actions.create_use_of_product, name="add_item_in_use"),
    path('actualizar_equipo_uso/<int:id_product>/<int:id_product_use>', actions.update_use_of_product, name="alter_item_in_use"),
    path('modificar_equipo/<int:id_item>', actions.update_item, name="update_item"),
    path('modificar_venta/<int:id_sale>', actions.update_sale, name="update_sale"),
    path('modificar_renta/<int:id_rent>', actions.update_rent, name="update_rent"),
    path('eliminar_producto/<id_product>', actions.delete_product, name="delete_product"),

]