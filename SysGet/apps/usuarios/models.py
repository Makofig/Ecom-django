from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    dni = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.username} - {self.first_name} - {self.last_name}";


class Cuenta(models.Model): 
    id = models.AutoField(primary_key=True); 
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cuenta');  
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00);  
    fecha_creacion = models.DateTimeField(auto_now_add=True); 

    def __str__(self):
        return f"Cuenta de {self.usuario.username} - Saldo: {self.monto}"

class Transferencia(models.Model): 

    id = models.AutoField(primary_key=True);  
    cuenta_origen = models.ForeignKey('Cuenta', on_delete=models.CASCADE, related_name='transferencias_realizadas'); 
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='transferencias_usuario');
    cuenta_destino = models.ForeignKey('Cuenta', on_delete=models.CASCADE, related_name='transferencias_recibidas'); 
    monto = models.DecimalField(max_digits=10, decimal_places=2); 
    fecha_transferencia = models.DateTimeField(auto_now_add=True); 

    def __str__(self):
        return (f"De {self.cuenta_origen.usuario.username} a "
                f"{self.cuenta_destino.usuario.username} - Monto: {self.monto}")
    
