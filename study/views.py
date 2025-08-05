from django.shortcuts import render

# Create your views here.
def material_estudio(request):
    print("Accediendo a material de estudio")
    return render(request, 'material_estudio.html')


