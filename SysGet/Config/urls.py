from django.contrib import admin
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as django_views 
from . import views

# Configurar el manejador de error 404
handler404 = 'Config.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.loginUser, name="login"),
    #path('', django_views.LoginView.as_view(template_name ="base/login.html"), name="login"),  
    path('logout/', django_views.logout_then_login, name="logout"), 
    path('inicio/', views.inicio, name="inicio"), #inicio de la pagina
    path('register/', views.registerUser, name="register"),

    #incluir las rutas desde usuarios 
    path('usuario/', include('apps.usuarios.urls')), 

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

