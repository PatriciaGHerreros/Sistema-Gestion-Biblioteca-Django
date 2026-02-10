from django.db import models
from django.contrib.auth.models import User


# Crear los modelos: Autor, Editorial y Libro

class Autor(models.Model):
    nombre = models.CharField(max_length=150)
    biografia = models.TextField(blank=True, null=True) # Opcional 

    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    nombre = models.CharField(max_length=150)
    pais = models.CharField(max_length=100, blank=True, null=True) # Opcional 

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    sinopsis = models.TextField()
    fecha_publicacion = models.DateField()
    
    # Portada: obligatoria en el modelo pero permitimos blank=True para no obligar en el form si no quieres
    # Pide manejar archivos multimedia
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)

    # Relaciones
    # Un libro tiene UN autor (si se borra el autor, se borran sus libros)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    
    # Un libro puede tener UNA editorial (que es opcional)
    # Si se borra la editorial, el libro NO se borra (SET_NULL)
    editorial = models.ForeignKey(Editorial, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo
     # Creamos funcion para ver si un libro esta disponible. Si existe algún alquiler de este libro impedir que se alquile. Si no existe ningún alquiler o el alquiler ha sido devuelto, permitir alquilarlo.
    def esta_disponible(self):
               
        alquiler_activo = Alquiler.objects.filter(libro=self, estado='alquilado').exists()
        
        return not alquiler_activo
    
class Alquiler(models.Model):
    # Opciones para el estado del alquiler
    ESTADO_CHOICES = [
        ('alquilado', 'Alquilado'),
        ('devuelto', 'Devuelto'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE) 
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_devolucion_prevista = models.DateField() 
    fecha_devolucion_real = models.DateField(null=True, blank=True) 
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='alquilado') 

    def __str__(self):
        return f"{self.usuario.username} alquiló {self.libro.titulo}"