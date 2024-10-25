from django.shortcuts import render 

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

def login(request):

    #print(request.__dict__) #permite recuperar los parametros en forma de diccionario
    #print(request.GET) # paramtros get 
    #recuperamos la informacion 
    #email = request.GET.get("email", default = None)
    #password = request.GET.get("password", default = None) 
    #print (email, password) 

    #para metodo POST 
    if request.method == "POST": 

        email = request.POST.get("email", default = None)
        password = request.POST.get("password", default = None) 


    return render(request, 'base/login.html', {})
