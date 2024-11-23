from django.shortcuts import render, redirect
from .forms import FormUsuario, FormUser
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

# Create your views here.
@login_required # Permite proteger la vista 
def dashboardUser(request):
    contexto = {
    } 
    return render(request,'dashboard.html', contexto);

""" Vistas Basadas en clases """
"""
class Nuevo(CreateView): 
    template_name = 'includes/form.html';
    model = Usuario;    
    form_class = FormUser;
    success_url = reverse_lazy('usuario:info');

    def get_context_data(self, **kwargs):
        contexto = super(Nuevo, self).get_context_data(**kwargs);
        contexto["titulo"] = "Nuevo Usuario"; 
        return contexto 

"""
"""
class Lista(ListView): 
    template_name = "usuario/info.html";
    model = Usuario; 
    context_object_name = "usuarios"; 
    paginate_by = 10; 

    def get_context_data(self, **kwargs):
        contexto = super(Lista, self).get_context_data(**kwargs);
        contexto["titulo"] = "Nuevo Usuario"; 
        return contexto 
    
    def get_queryset(self):
        query = self.model.objects.all()
        nombre = self.request.GET.get('nombre', None) 
        if nombre: 
            query = query.filter(nombre=nombre)
        return query.order_by("apellido");
"""
@login_required # Permite proteger la vista 
def nuevoUser(request):
    #form = FormUsuario();
    form = FormUser();
    message = None; 
    if request.method == "POST": 
        form = FormUser(request.POST);
        if form.is_valid(): 
            print ("correcto");
            form.save();
            return redirect('usuario:info');
        else: 
            message = "No se pudo gurdar el usuario."; 
     
    contexto = {
         "form": form, 
         "message": message, 
    } 
    return render(request,'includes/form.html', contexto);

@login_required # Permite proteger la vista  
def infoUser(request):

    #usuario = Usuario.objects.all();
    #usuario = Usuario.objects.filter(username = "markos").first();
    usuario = Usuario.objects.all()
    print (usuario);  
    #print (usuario.count()); 

    contexto = {
        "usuario": usuario, 
    }
    return render(request,'usuario/info.html', contexto); 

@login_required # Permite proteger la vista 
def profileUser(request):
    return render(request,'profileUser.html');
