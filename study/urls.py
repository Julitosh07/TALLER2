from django.urls import path
from django.views.generic import TemplateView
from examenes import views

app_name = 'study'
urlpatterns = [
    path('material_estudio/', views.material_estudio, name='material_estudio'),
]