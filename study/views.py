from django.shortcuts import render
from .models import Subtema, MaterialEstudio, UserMaterialEstudio
from examenes.models import Category, Subject

# Create your views here.
def material_estudio(request):
    categorias = Category.objects.all()
    return render(request, 'material_estudio.html', {'categorias': categorias})


def material_estudio_categoria(request, category_id):
    materiales_estudio = MaterialEstudio.objects.filter(subtema__subject__categoria_id=category_id).all()
    context = {'materiales_estudio': materiales_estudio}
    user = request.user
    if user and user.is_authenticated:
        materiales_estudio_visto = UserMaterialEstudio.objects.filter(usuario=user, visto=True).all()
        if materiales_estudio_visto:
            material_estudio_visto = [material.materiales.id for material in materiales_estudio_visto]

            context['materiales_estudio_visto'] = material_estudio_visto
    print('material_estudio', material_estudio)

    return render(request, 'material_estudio_categoria.html', context)

def material_estudio_detail(request, material_estudio_id):
    user = request.user
    material = MaterialEstudio.objects.get(pk=material_estudio_id)

    if user.is_authenticated:
        if not UserMaterialEstudio.objects.filter(usuario=user, materiales=material).exists():
            usr_material = UserMaterialEstudio.objects.create(usuario=user, materiales=material)
            usr_material.visto = True
            usr_material.save()

    return render(request, 'material_estudio_detail.html', {'material': material})
