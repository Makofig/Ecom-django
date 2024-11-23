from django.contrib import admin

from .models import Usuario, Cuenta, Transferencia
# Register your models here.

admin.site.register(Usuario);
admin.site.register(Cuenta);
admin.site.register(Transferencia); 