from django.urls import path, include


from . import views

app_name = "usuario"

urlpatterns = [
    #path('dashboard/', views.dashboardUser, name="dashboard"), 
    path('info/', views.infoUser, name="info"), 
    path('listar/', views.ListaUser.as_view(), name="listar"), 
    path('profile/', views.profileUser, name="profile"), 
    path('profile/', views.profileUser, name="profile"),
    #path('crear/', views.CrearUser, name="crear"), 
    path('crear/', views.CrearUser.as_view(),  name="crear"),
    #path('info/', views.Lista.as_view(),  name="info"), 
    path('<int:pk>/editar/', views.UpdateUser.as_view(), name='editar'), 
    path('<int:pk>/', views.DetailUser.as_view(), name='detalle'),
    path('<int:pk>/delete', views.DeleteUser.as_view(), name='delete'),  

    # rutas para cuentas 
    path('cuenta/', views.InfoCuenta.as_view(), name='cuenta'),
    path('cuenta/<int:pk>/editar/', views.UpdateCuenta.as_view(), name='editarCuenta'),
    path('cuenta/crear/', views.CrearCuenta.as_view(), name='crearCuenta'),
    path('cuenta/listar/', views.ListarCuenta.as_view(), name='listarCuenta'),
    path('cuenta/<int:pk>/delete', views.DeleteCuenta.as_view(), name='deleteCuenta'), 

    # rutas para las transferencias 
    path('transferencia/', views.InfoTransferencias.as_view(), name='listarTransferencias'),
    path('transferencia/realizar/', views.CrearTransferencias.as_view(), name='realizarTransferencia'),

]