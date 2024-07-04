from django.urls import path
from . import views
from app.crud import posts, put, delete
from django.conf import settings

app_name = 'app'

urlpatterns = [
    path('', views.login_view, name="signin"),
    path('cerrar_sesion', views.logout_, name="signout"),
    path('herramientas', views.index, name="tools"),
    path('equipos', views.items, name="items"),
    path('ventas', views.sales, name="sales"),
    path('rentas', views.rents, name="rents"),
    path('historial', views.history, name="history"),

    path(r'herramientas/<id_tool>', views.tool_view, name="tool"),
    path(r'equipos/<id_item>', views.item_view, name="item"),
    path(r'movimiento/<int:option>/<int:id_mov>', views.movement_view, name="movement"),


    path('agregar-proveedor/<path_>', posts.add_supplier, name="add_supplier"),
    # path('agregar_herramienta', posts.create_tool, name="add_tool"),
    path('agregar_producto', posts.create_product, name="add_product"),
    path('agregar_transaccion_herramienta/<int:id>', posts.register_transaction_tool, name="add_transaction_tool"),
    path('agregar_transaccion_equipo/<int:id>', posts.register_transaction_item, name="add_transaction_item"),
    path('agregar_uso_producto/<int:id>', posts.dispose_product, name="dispose_product"),

    path('modificar_herramienta/<int:id_tool>', put.update_tool, name="update_tool"),
    path('actualizar_equipo_uso/<int:id_product>/<int:id_product_use>', put.update_use_of_product, name="alter_item_in_use"),
    path('actualizar_estado_producto/<int:id_product>/<int:id_product_state>', put.edit_state_product, name="alter_state_product"),
    path('modificar_equipo/<int:id_item>', put.update_item, name="update_item"),
    path('modificar_venta/<int:id_sale>', put.update_sale, name="update_sale"),
    path('modificar_renta/<int:id_rent>', put.update_rent, name="update_rent"),
    path(r'devolver_producto/<int:id_rent>', put.return_rent, name="return_rent"),
    path(r'cancelar_venta/<int:id_sale>', put.cancel_sale, name="cancel_sale"),
    path(r'cancelar_renta/<int:id_rent>', put.cancel_rent, name="cancel_rent"),
    # path('agregar_equipo', actions.create_item, name="add_item"),
    path('eliminar_producto/<id_product>', delete.delete_product, name="delete_product"),
]

if settings.DEBUG:
    urlpatterns.append(path('registrar_usuario', views.signup_view, name="signup"))