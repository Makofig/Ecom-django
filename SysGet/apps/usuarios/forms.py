from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Usuario, Cuenta, Transferencia

class FormUsuario(forms.ModelForm): 

    class Meta: 
        model = Usuario
        fields = ["password", "username", "first_name", "last_name", "email", "dni"]

class FormUser(UserCreationForm):  

    #atributo1 = forms.CharField(); 
    #username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ingrese un nombre de usuario'})); 
    class Meta: 
        model = Usuario
        fields = ["username", "first_name", "last_name", "email", "dni", "password1", "password2", "photo", "is_active"]

    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs); 
        campos = ["first_name", "last_name", "email", "dni", "password1", "password2", "photo", "is_active"]; 
        self.fields["username"].widget.attrs={'class': "block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6", 'placeholder': 'janesmith'}
        for valor in campos: 
            self.fields[valor].widget.attrs["class"] = "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6";
        
     

    def clean_dni(self): 
        dni = self.cleaned_data["dni"]; 
        if not (7<=len(str(dni))<=8): 
            raise ValidationError("El DNI debe tener entre 7 y 8 digitos"); 

        return dni; 

class FormCuenta(forms.ModelForm): 

    class Meta: 
        model = Cuenta 
        fields = ["alias", "monto"]

    def __init__(self, *args, **kwargs):
        super(FormCuenta, self).__init__(*args, **kwargs); 
        self.fields["alias"].widget.attrs={'class': "block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6", 'placeholder': 'janesmith'}
        self.fields["monto"].widget.attrs={'class': "block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6", 'placeholder': '1000'} 

    def clean_alias(self):
        alias = self.cleaned_data.get('alias', '').strip()  # Obtener el alias ingresado
        suffix = '.dest.mk'
        if not alias.endswith(suffix):
            alias = f"{alias}{suffix}"  # Agregar el sufijo si no está presente
        return alias
       

class FormTransferencia(forms.ModelForm): 

    class Meta: 
        model = Transferencia 
        fields = ["monto", "motivo", "cuenta_origen", "cuenta_destino"]   

    def __init__(self, *args, **kwargs):
        super(FormTransferencia, self).__init__(*args, **kwargs); 
        #monto_actual = self.instance.monto if self.instance and self.instance.pk else ''
        
        self.fields["monto"].widget.attrs={'class': "block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6", 'placeholder': '100'}
        self.fields["motivo"].widget.attrs={'class': "block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6", 'placeholder': '1000'}
        self.fields["cuenta_destino"].widget.attrs={'class': "block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6", 'placeholder': '1000'} 
        self.fields["cuenta_origen"].widget.attrs={'class': "block flex-1 border-0 bg-transparent py-1.5 pl-1 text-gray-900 placeholder:text-gray-400 focus:ring-0 sm:text-sm/6", 'placeholder': '1000'}  


       