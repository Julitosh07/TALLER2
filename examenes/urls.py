from django.urls import path
from django.views.generic import TemplateView
from examenes import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro', views.registro_estudiante, name='registro_estudiante'),
    path('simulacro/<int:estudiante_id>/', views.simulacro_view, name='simulacro'),
    path('simulacro/<int:estudiante_id>/categoria/<int:categoria_id>/', views.ver_preguntas_categoria, name='ver_preguntas_categoria'),
    path('resultado', TemplateView.as_view(template_name='resultado.html'), name='resultado'),
    path('material_estudio/', views.material_estudio, name='material_estudio'),
    
]