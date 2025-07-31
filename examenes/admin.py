from django.contrib import admin

# Register your models here.
from .models import Category, Subject, Question, User, Exam, Answer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):  
    list_display = ('nombre', 'categoria')
    search_fields = ('nombre',)
    list_filter = ('categoria',)
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('enunciado_corto', 'materia', 'respuesta_correcta')
    search_fields = ('enunciado', 'materia__nombre')
    list_filter = ('materia',)
    
    def enunciado_corto(self, obj):
        return obj.enunciado[:50] + "..."
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'documento', 'correo', 'colegio', 'grado')
    search_fields = ('nombre', 'documento', 'correo')
    list_filter = ('colegio', 'grado')
    
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'fecha', 'puntuacion')
    search_fields = ('estudiante__nombre', 'estudiante__documento')
    list_filter = ('fecha',)
    
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('examen', 'pregunta_resumen', 'respuesta_usuario', 'es_correcta')
    list_filter = ('es_correcta',)
    search_fields = ('pregunta__enunciado', 'examen__estudiante__nombre')

    def pregunta_resumen(self, obj):
        return obj.pregunta.enunciado[:50] + "..."
