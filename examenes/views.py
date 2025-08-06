from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Subject, Question, User, Exam, Answer
from .forms import UserForm
from django.db.models import Count, Avg

# Create your views here.

def index(request):
    categorias = Category.objects.all()
    return render(request, 'index.html', {'categorias': categorias})


def dashboard_view(request):
    total_examenes = Exam.objects.count()
    promedio_por_materia = Subject.objects.annotate(
        promedio=Avg('question__answer__es_correcta')
    )
    materias = []
    for materia in promedio_por_materia:
        materias.append(
            {
                "promedio": materia.promedio * 10,
                "nombre": materia.nombre
            }
        )

    context = {
        'total_examenes': total_examenes,
        'promedio_por_materia': materias,
    }
    return render(request, 'dashboard.html', context)

def registro_estudiante(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            documento = form.cleaned_data['documento']
            
            if User.objects.filter(documento=documento, ya_presento=True).exists():
                return render(request, 'resultado.html')
            
            estudiante, creado = User.objects.get_or_create(documento=documento, defaults=form.cleaned_data)
            
            if not creado:
                for campo, valor in form.cleaned_data.items():
                    setattr(estudiante, campo, valor)
                estudiante.save()
                
            return redirect('simulacro', estudiante_id=estudiante.id)
    else:
        form = UserForm()
    
    return render(request, 'registro_estudiante.html', {'form': form})

def simulacro_view(request, estudiante_id):
    estudiante = get_object_or_404(User, id=estudiante_id)
    categorias = Category.objects.all()

    # Reiniciar la sesión si es un nuevo estudiante o no ha respondido nada
    if 'estudiante_id' not in request.session or request.session['estudiante_id'] != estudiante.id:
        request.session['estudiante_id'] = estudiante.id
        request.session['categorias_respondidas'] = []
        request.session['respuestas_parciales'] = {}
        request.session['examen_guardado'] = False
        request.session.modified = True

    respondidas = request.session.get("categorias_respondidas", [])

    # Guardar el examen si ya respondió todas
    if len(respondidas) == categorias.count():
        if not request.session.get("examen_guardado"):
            respuestas_parciales = request.session.get("respuestas_parciales", {})

            examen = Exam.objects.create(estudiante=estudiante)
            correctas = 0
            total = 0

            for respuestas in respuestas_parciales.values():
                for pregunta_id, seleccion in respuestas.items():
                    pregunta = Question.objects.get(id=pregunta_id)
                    es_correcta = seleccion == pregunta.respuesta_correcta
                    if es_correcta:
                        correctas += 1
                    total += 1

                    Answer.objects.create(
                        examen=examen,
                        pregunta=pregunta,
                        respuesta_usuario=seleccion,
                        es_correcta=es_correcta
                    )

            if total > 0:
                examen.puntuacion = round((correctas / total) * 100, 2)
                examen.save()

            estudiante.ya_presento = True
            estudiante.save()

            request.session['examen_guardado'] = True
            request.session.modified = True

            return render(request, 'resultado.html', {'puntuacion': examen.puntuacion, 'estudiante': estudiante})
        
        else:
            examen = Exam.objects.filter(estudiante=estudiante).last()
            if examen:
                puntuacion = examen.puntuacion
            else:
                puntuacion = 0

            return render(request, 'simulacro.html', {
                'puntuacion': puntuacion,
                'estudiante': estudiante,
                'categorias': categorias,
                'respondidas': respondidas,
            })

    return render(request, 'simulacro.html', {
        'estudiante': estudiante,
        'categorias': categorias,
        'respondidas': respondidas,
    })

    

def ver_preguntas_categoria(request, estudiante_id, categoria_id):
    estudiante = get_object_or_404(User, id=estudiante_id)
    categoria = get_object_or_404(Category, id=categoria_id)
    preguntas = Question.objects.filter(materia__categoria=categoria)

    # Validar que no repita categoría
    respondidas = request.session.get('categorias_respondidas', [])
    if categoria_id in respondidas:
        return redirect('simulacro', estudiante_id=estudiante.id)

    if request.method == 'POST':
        respuestas = {}
        for pregunta in preguntas:
            seleccion = request.POST.get(f'pregunta_{pregunta.id}')
            if seleccion:
                respuestas[str(pregunta.id)] = seleccion

        if respuestas:
            # Guardar respuestas en sesión
            if 'respuestas_parciales' not in request.session:
                request.session['respuestas_parciales'] = {}

            request.session['respuestas_parciales'][str(categoria_id)] = respuestas

            # Registrar categoría respondida
            if 'categorias_respondidas' not in request.session:
                request.session['categorias_respondidas'] = []
            request.session['categorias_respondidas'].append(categoria_id)

            request.session.modified = True

            return redirect('simulacro', estudiante_id=estudiante.id)

    context = {
        'estudiante': estudiante,
        'categoria': categoria,
        'preguntas': preguntas,
    }
    return render(request, 'ver_preguntas_categoria.html', context)



def responder_categoria(request, categoria_id):
    categoria = get_object_or_404(Category, id=categoria_id)
    preguntas = Question.objects.filter(categoria=categoria)
    
    # Inicializar el historial en sesión si no existe
    if "categorias_respondidas" not in request.session:
        request.session["categorias_respondidas"] = []

    if categoria_id in request.session["categorias_respondidas"]:
        return redirect("seleccionar_categoria")  # No permite repetir

    if request.method == "POST":
        respuestas = {}
        for pregunta in preguntas:
            seleccion = request.POST.get(f"pregunta_{pregunta.id}")
            if seleccion:
                respuestas[pregunta.id] = seleccion

        if respuestas:
            if "respuestas_parciales" not in request.session:
                request.session["respuestas_parciales"] = {}

            request.session["respuestas_parciales"][str(categoria_id)] = respuestas
            request.session.modified = True  

            request.session["categorias_respondidas"].append(categoria_id)
            request.session.modified = True

            return redirect("seleccionar_categoria")

    return render(request, "responder_categoria.html", {
        "categoria": categoria,
        "preguntas": preguntas,
    })


