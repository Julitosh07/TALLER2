from django.db import models

# Create your models here.
class Category(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorias"
    
class Subject(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"
    
    class Meta:
        verbose_name_plural = "Materias"
    
    
class Question(models.Model):
    enunciado = models.TextField()
    materia = models.ForeignKey(Subject, on_delete=models.CASCADE)
    opcion_a = models.CharField(max_length=255)
    opcion_b = models.CharField(max_length=255)
    opcion_c = models.CharField(max_length=255)
    opcion_d = models.CharField(max_length=255)
    
    OPCIONES = [
        ('A', 'Opción A'),  
        ('B', 'Opción B'),
        ('C', 'Opción C'),
        ('D', 'Opción D'),
    ]
    respuesta_correcta = models.CharField(max_length=1, choices=OPCIONES)
    
    def __str__(self):
        return f"Pregunta: {self.enunciado[:50]}... - Respuesta: {self.respuesta_correcta}"  
    
    class Meta:
        verbose_name_plural = "Preguntas"


class User(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)  # Cédula o TI
    correo = models.EmailField(unique=True)
    colegio = models.CharField(max_length=100, blank=True)
    grado = models.CharField(max_length=50, blank=True)
    
    ya_presento = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombre} ({self.documento})'
    
    class Meta:
        verbose_name_plural = "Usuarios"
    

class Exam(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    puntuacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    preguntas = models.ManyToManyField(Question, through='Answer')

    def __str__(self):
        return f'Examen de {self.estudiante.nombre} - {self.estudiante.documento} - {self.fecha.strftime("%Y-%m-%d")}'
    
    class Meta:
        verbose_name_plural = "Examenes"
    

class Answer(models.Model):
    examen = models.ForeignKey(Exam, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Question, on_delete=models.CASCADE)
    respuesta_usuario = models.CharField(max_length=1, choices=Question.OPCIONES)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return f'Respuesta de {self.examen.estudiante.nombre} a "{self.pregunta}"'
    
    class Meta:
        verbose_name_plural = "Respuestas"