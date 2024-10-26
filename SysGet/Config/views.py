from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login 
from django.http import HttpResponse

def inicio(request):
    lista_usuarios = [
        {"nombre": "Marcos", "apellido": "Aquino"},
        {"nombre": "Mario", "apellido": "Aquino"},
        {"nombre": "Lujan", "apellido": "Aquino"},
    ] 
    contex = {
        "allUser": lista_usuarios
    }
    return render(request, 'index.html', contex)

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
