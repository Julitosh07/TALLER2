from django.contrib import admin
from .models import Subtema, MaterialEstudio, UserMaterialEstudio

# Register your models here.
@admin.register(Subtema)
class SubtemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'subject')
    list_filter = ('subject',)            
    search_fields = ('nombre',)           

@admin.register(MaterialEstudio)
class MaterialEstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'subtema', 'tipo')
    list_filter = ('tipo', 'subtema')
    search_fields = ('titulo', 'descripcion')