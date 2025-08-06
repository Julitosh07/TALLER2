from django.shortcuts import render
from .models import Subtema, MaterialEstudio
from examenes.models import Category, Subject

# Create your views here.
def material_estudio(request):
    categorias = Category.objects.all()
    return render(request, 'material_estudio.html', {'categorias': categorias})


def material_estudio_categoria(request, category_id):
    materiales_estudio = MaterialEstudio.objects.filter(subtema__subject__categoria_id=category_id).all()

    print('material_estudio', material_estudio)

    return render(request, 'material_estudio_categoria.html', {'materiales_estudio': materiales_estudio})

def material_estudio_detail(request, material_estudio_id):
    material = MaterialEstudio.objects.get(pk=material_estudio_id)
    return render(request, 'material_estudio_detail.html', {'material': material})
