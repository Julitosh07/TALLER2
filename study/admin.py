from django.contrib import admin
from .models import Subtema, MaterialEstudio

# Register your models here.
@admin.register(Subtema)
class SubtemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'subject')
    list_filter = ('subject',)            
    search_fields = ('nombre',)           

@admin.register(MaterialEstudio)
class MaterialEstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtema', 'tipo', 'visto')
    list_filter = ('tipo', 'visto', 'subtema')
    search_fields = ('titulo', 'descripcion')