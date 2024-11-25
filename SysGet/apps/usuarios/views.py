from django.shortcuts import render, redirect
from .forms import FormUsuario, FormUser, FormCuenta, FormTransferencia

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.utils.timezone import now
from django.db import transaction
from django.core.exceptions import ValidationError

from django.urls import reverse_lazy

from .models import Usuario, Cuenta, Transferencia

# Create your views here.
"""
@login_required # Permite proteger la vista 
def dashboardUser(request):
    contexto = {
    } 
    return render(request,'dashboard.html', contexto);
"""
""" Vistas Basadas en clases """

class CrearUser(CreateView): 
    template_name = 'usuario/create.html'
    model = Usuario
    form_class = FormUser
    second_form_class = FormCuenta
    print (f"--->", form_class); 
    success_url = reverse_lazy('usuario:info')
    
    # Aplicar login_required usando method_decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Procesar ambos formularios en el método POST
        form_user = self.form_class(request.POST, request.FILES)
        form_cuenta = self.second_form_class(request.POST)
        
        if form_user.is_valid() and form_cuenta.is_valid():
            return self.form_valid(form_user, form_cuenta)
        else:
            return self.form_invalid(form_user, form_cuenta)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form_cuenta' not in context:
            context['form_cuenta'] = self.second_form_class()
        context['titulo'] = "Nuevo Usuario"
        context['usuario'] = self.request.user
        return context
        
    def form_valid(self, form_user, form_cuenta):
        usuario = form_user.save(commit=False)
        usuario.is_active = True
        usuario.save()

        # Crear la cuenta asociada al usuario
        cuenta = form_cuenta.save(commit=False)
        cuenta.usuario = usuario
        cuenta.save()

        return super().form_valid(form_user)
    
    def form_invalid(self, form_user, form_cuenta):
        # Volver a renderizar la página con los errores
        context = self.get_context_data(form=form_user, form_cuenta=form_cuenta)
        return self.render_to_response(context)


class ListaUser(ListView): 
    template_name = "usuario/listar.html";
    model = Usuario; 
    context_object_name = "usuarios"; 
    paginate_by = 20; 

    def get_context_data(self, **kwargs):
        context = super(ListaUser, self).get_context_data(**kwargs);
        context["titulo"] = "Nuevo Usuario"; 
        context['usuario'] = self.request.user
        return context 
    
    def get_queryset(self):
        query = self.model.objects.all()
        nombre = self.request.GET.get('nombre', None)
        if nombre:
            # Busca en el campo `first_name` o `last_name`
            query = query.filter(first_name__icontains=nombre) | query.filter(last_name__icontains=nombre)
        return query.order_by("last_name")


class UpdateUser(UpdateView):
    model = Usuario
    fields = ['username', 'first_name', 'last_name', 'email', 'dni', 'photo']
    template_name = 'usuario/editar.html'
    success_url = reverse_lazy('usuario:info') 
    #pk_url_kwarg = "id_user"

    # Aplicar login_required usando method_decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class DetailUser(DetailView): 
    model = Usuario
    template_name = 'usuario/detalle.html'

    # Aplicar login_required usando method_decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class DeleteUser(DeleteView): 
    model = Usuario
    template_name = 'usuario/delete.html'
    success_url = reverse_lazy('usuario:listar')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

"""
@login_required # Permite proteger la vista 

def CrearUser(request):
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
"""
@login_required # Permite proteger la vista  
def infoUser(request):

    #usuario = Usuario.objects.all();
    #usuario = Usuario.objects.filter(username = "markos").first();
    #usuario = Usuario.objects.all()
    usuario = request.user
    print (usuario);  
    #print (usuario.count()); 

    contexto = {
        "usuario": usuario, 
    }
    return render(request,'usuario/info.html', contexto); 

@login_required # Permite proteger la vista 
def profileUser(request):
    return render(request,'profileUser.html');


#Cuentas 

class InfoCuenta(ListView): 
    template_name = "cuenta/info.html";
    model = Cuenta; 
    context_object_name = "cuenta"; 
    #aginate_by = 10; 

    def get(self, request, *args, **kwargs):
        cuenta = None
        if hasattr(request.user, 'cuenta'):  
            cuenta = request.user.cuenta

        context = {
            'cuenta': cuenta,
            'usuario': request.user, 
        }
        return render(request, self.template_name, context)
    
    def get_queryset(self):
        query = self.model.objects.all()
        nombre = self.request.GET.get('nombre', None) 
        if nombre: 
            query = query.filter(nombre=nombre)
        return query;

class CrearCuenta(CreateView): 
    template_name = 'cuenta/create.html'
    model = Cuenta
    form_class = FormCuenta 
    print (f"--->", form_class); 
    success_url = reverse_lazy('usuario:cuenta')
    
    # Aplicar login_required usando method_decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        contexto = super(CrearCuenta, self).get_context_data(**kwargs)
        contexto["titulo"] = "Nuevo Cuenta"; 
        return contexto
    
    def form_valid(self, form):
        cuenta = form.save(commit=False)
        cuenta.usuario = self.request.user  # Asociar la cuenta al usuario actual
        cuenta.save()
        return super().form_valid(form)

class UpdateCuenta(UpdateView):
    model = Cuenta
    fields = ['monto']
    template_name = 'cuenta/editar.html'
    success_url = reverse_lazy('usuario:cuenta') 
    #pk_url_kwarg = "id_user"

    # Aplicar login_required usando method_decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Sobrescribimos get_context_data para incluir datos adicionales en el contexto.
        """
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        return context

class ListarCuenta(ListView):
    template_name = "cuenta/listar.html";
    model = Cuenta; 
    context_object_name = "cuentas"; 
    paginate_by = 20; 

    def get_context_data(self, **kwargs):
        context = super(ListarCuenta, self).get_context_data(**kwargs); 
        context['usuario'] = self.request.user
        return context 
    
    def get_queryset(self):
        query = self.model.objects.all()
        nombre = self.request.GET.get('nombre', None)
        if nombre:
            # Busca en el campo `first_name` o `last_name`
            query = query.filter(alias__icontains=nombre) 
        return query.order_by("fecha_creacion")

class DeleteCuenta(DeleteView): 
    model = Cuenta
    template_name = 'cuenta/delete.html'
    success_url = reverse_lazy('usuario:listarCuenta')

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# Transferencias 


class InfoTransferencias(ListView):
    template_name = "transferencias/listar.html";
    model = Transferencia; 
    context_object_name = "transferencias"; 
    aginate_by = 20; 

    def get_context_data(self, **kwargs):
        """
        Sobrescribimos get_context_data para incluir datos adicionales en el contexto.
        """
        context = super().get_context_data(**kwargs)
        cuenta = getattr(self.request.user, 'cuenta', None)  
        context['cuenta'] = cuenta
        context['usuario'] = self.request.user
        return context

    def get_queryset(self):
        """
        Filtrar las transferencias asociadas a la cuenta del usuario actual.
        """
        if not hasattr(self.request.user, 'cuenta'):  # Verificar si el usuario tiene una cuenta asociada
            return Transferencia.objects.none()  # Retornar queryset vacío si no tiene cuenta

        cuenta = self.request.user.cuenta
        query = Transferencia.objects.filter(
            Q(cuenta_origen=cuenta) | Q(cuenta_destino=cuenta)
        )

        # Filtrar por nombre, si el parámetro existe
        nombre = self.request.GET.get('nombre', None)
        if nombre:
            query = query.filter(usuario__username__icontains=nombre)  # Busca por nombre del usuario relacionado

        return query.order_by('-fecha_transferencia')  # Ordenar las transferencias por fecha (descendente)
    
class CrearTransferencias(CreateView):
    template_name = 'transferencias/create.html'
    model = Transferencia
    form_class = FormTransferencia 
    success_url = reverse_lazy('usuario:listarTransferencias')
    
    # Aplicar login_required usando method_decorator
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        contexto = super(CrearTransferencias, self).get_context_data(**kwargs)
        contexto["titulo"] = "Nuevo Cuenta"; 
        return contexto
    
    def get_form(self, *args, **kwargs):
        """
        Limitar las opciones de cuenta_origen a la cuenta del usuario logueado.
        """
        form = super().get_form(*args, **kwargs)
        if hasattr(self.request.user, 'cuenta'):
            form.fields['cuenta_origen'].queryset = Cuenta.objects.filter(usuario=self.request.user)
        return form

    def form_valid(self, form):
        cuenta_origen = form.instance.cuenta_origen
        print(cuenta_origen)
        monto_transferencia = form.cleaned_data['monto']
        
        # Validar que el monto no exceda el saldo actual
        if cuenta_origen.monto < monto_transferencia:
            form.add_error('monto', 'El monto no puede ser superior al saldo disponible.')
            return self.form_invalid(form)

        # Asignar usuario logueado y fecha actual
        form.instance.usuario = self.request.user
        form.instance.fecha_transferencia = now()
        
        # Actualizar saldos en una transacción para asegurar consistencia
        with transaction.atomic():
            # Descontar monto de la cuenta origen
            cuenta_origen.monto -= monto_transferencia
            cuenta_origen.save()

            # Sumar monto a la cuenta destino
            cuenta_destino = form.instance.cuenta_destino
            cuenta_destino.monto += monto_transferencia
            cuenta_destino.save()

        return super().form_valid(form)