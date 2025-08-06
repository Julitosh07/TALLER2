from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'study'
urlpatterns = [
    path('material_estudio/', views.material_estudio, name='material_estudio'),
    path('material_estudio/<int:category_id>', views.material_estudio_categoria, name='material_estudio_categoria'),
    path('material_estudio_detail/<int:material_estudio_id>', views.material_estudio_detail, name='material_estudio_detail'),
]