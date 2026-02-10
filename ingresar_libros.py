import os
import django
import random
from faker import Faker
import requests  # Para descargar la imagen
from django.core.files import File  # Para que Django gestione el archivo
from tempfile import NamedTemporaryFile  # Para guardar la imagen temporalmente

# 1. Configuramos el entorno de Django para que este script pueda "hablar" con la base de datos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_project.settings')
django.setup()

# Importamos los  modelos (OJO: Esto debe ir DESPUÉS de django.setup)
from biblioteca.models import Autor, Editorial, Libro

# Instancia de Faker en español
fake = Faker('es_ES')

def crear_datos():
    print("🧹 Limpiando base de datos...")
    Libro.objects.all().delete()
    Autor.objects.all().delete()
    Editorial.objects.all().delete()
    print("🌱 Iniciando la creación de datos con imágenes...")

    # --- PASO 1: CREAR AUTORES ---
    autores = [Autor.objects.create(nombre=fake.name(), biografia=fake.text(max_nb_chars=200)) for _ in range(10)]
    print(f"✅ {len(autores)} autores creados.")

    # --- PASO 2: CREAR EDITORIALES ---
    editoriales = [Editorial.objects.create(nombre=fake.company(), pais=fake.country()) for _ in range(5)]
    print(f"✅ {len(editoriales)} editoriales creadas.")

    # --- PASO 3: CREAR LIBROS CON PORTADA ---
    print("Creando libros y descargando portadas (esto puede tardar un poco)...")
    for i in range(25):
        autor_random = random.choice(autores)
        editorial_random = random.choice(editoriales)
        
        # Creamos la instancia del libro sin guardar la foto todavía
        libro = Libro(
            titulo=fake.catch_phrase().title(),
            sinopsis=fake.paragraph(nb_sentences=5),
            fecha_publicacion=fake.date_between(start_date='-10y', end_date='today'),
            autor=autor_random,
            editorial=editorial_random,
        )

        # Lógica de descarga de imagen
        try:
            # Usamos un servicio de imágenes aleatorias (400x600 px es ideal para libros)
            url_imagen = "https://loremflickr.com/400/600/book,library/all"
            response = requests.get(url_imagen, timeout=10)
            
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                
                # Guardamos la imagen en el campo 'portada'
                nombre_foto = f"portada_{random.randint(1000,9999)}.jpg"
                libro.portada.save(nombre_foto, File(img_temp), save=True)
            else:
                libro.save() # Si falla la imagen, guardamos el libro igualmente
        except Exception as e:
            print(f"No se pudo descargar la imagen para el libro {i+1}: {e}")
            libro.save()

    print("✅ 25 libros creados con sus portadas reales.")
    print("🎉 ¡Proceso finalizado con éxito!")

if __name__ == '__main__':
    crear_datos()