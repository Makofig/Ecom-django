from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.hashers import make_password
from apps.usuarios.models import Usuario

def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required # Permite proteger la vista 
def inicio(request):
    usuario = request.user
    contex = {
        "usuario": usuario
    }
    print(request.user); 
    return render(request, 'dashboard.html', contex)

def loginUser(request):

    #print(request.__dict__) #permite recuperar los parametros en forma de diccionario
    #print(request.GET) # paramtros get 
    #recuperamos la informacion 
    #email = request.GET.get("email", default = None)
    #password = request.GET.get("password", default = None) 
    #print (email, password) 

    #para metodo POST 
    username = ""
    if request.method == "POST": 

        username = request.POST.get("username", default = None)
        password = request.POST.get("password", default = None) 
        user = authenticate(request, username=username, password=password )
        print(user)
        if user is not None:
            # Iniciar sesión para este usuario
            login(request, user)
            return redirect('inicio/')
        else:
            # Si las credenciales son incorrectas
            error_menssage = "Usuario o contraseña incorrectos."
            contexto = {
                'error': error_menssage,
                'username': username, 
            }
            return render(request, 'base/login.html', contexto)
        
    return render(request, 'base/login.html', {})

def registerUser(request): 

    if request.method == "POST": 
        username = request.POST.get("username", default=None)
        firstname = request.POST.get("firstname", default=None)
        lastname = request.POST.get("lastname", default=None)
        email = request.POST.get("email", default=None)
        password = request.POST.get("password", default=None)
        is_active = request.POST.get("is_active", default=True)

        if username and email and password:
            # Crear y guardar el usuario con la contraseña encriptada
            try:
                user = Usuario(
                    username=username,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=make_password(password),  # Encriptar la contraseña
                    is_active = is_active,
                    
                )
                user.save()
                return render(request, 'base/login.html', {'user': user})
            except Exception as e:
                print(f"Error al crear el usuario: {e}")
                return render(request, 'base/register.html', {'error': 'Error al registrar el usuario'})
        else:
            return render(request, 'base/register.html', {'error': 'Todos los campos son obligatorios'})

    return render(request, 'base/register.html', {})

