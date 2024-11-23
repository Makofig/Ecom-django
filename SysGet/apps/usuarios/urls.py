from django.urls import path

from . import views

app_name = "usuario"

urlpatterns = [
    path('dashboard/', views.dashboardUser, name="dashboard"), 
    path('info/', views.infoUser, name="info"), 
    path('profile/', views.profileUser, name="profile"), 
    path('profile/', views.profileUser, name="profile"),
    path('nuevo/', views.nuevoUser, name="nuevo"), 
    #path('nuevo/', views.Nuevo.as_view(),  name="nuevo"),
    #path('info/', views.Lista.as_view(),  name="info"), 
]