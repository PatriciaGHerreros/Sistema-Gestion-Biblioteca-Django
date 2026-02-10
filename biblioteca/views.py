from django.shortcuts import render, redirect, get_object_or_404
from .forms import AutorForm, LibroForm, EditorialForm, RegistroForm
from .models import Libro, Autor, Editorial, Alquiler
from django.core.paginator import Paginator
from django.views.generic import ListView
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Creamos las vistas: lista de libros

def lista_libros(request):
    # 1. RECUPERAR LIBROS (BÚSQUEDA)
    # Obtenemos lo que el usuario ha escrito en el buscador (si hay algo)
    busqueda = request.GET.get('q') 

    if busqueda:
        # Si hay búsqueda, filtramos por título (icontains = contiene texto, ignora mayúsculas)
        libros_list = Libro.objects.filter(titulo__icontains=busqueda).order_by('-fecha_publicacion')
    else:
        # Si no hay búsqueda, traemos todos ordenados por fecha
        libros_list = Libro.objects.all().order_by('-fecha_publicacion')

    # 2. PAGINACIÓN
    paginator = Paginator(libros_list, 3) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'biblioteca/libro_lista.html', {
        'page_obj': page_obj,  # Ahora enviamos 'page_obj' en vez de 'libros'
        'busqueda': busqueda   # Enviamos el texto buscado para mantenerlo en la caja
    })
def crear_autor(request):
    if request.method == 'POST':
        # Si alguien envió datos (le dio a Guardar)
        formulario = AutorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            # De momento redirigimos a la lista de libros, luego lo cambiaremos
            return redirect('lista_libros')
    else:
        # Si entra por primera vez (GET), le mostramos el formulario vacío
        formulario = AutorForm()
    
    return render(request, 'biblioteca/autor_form.html', {'formulario': formulario})

def crear_editorial(request):
    if request.method == 'POST':
        formulario = EditorialForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('lista_libros')
    else:
        formulario = EditorialForm()
    
    return render(request, 'biblioteca/editorial_form.html', {'formulario': formulario})

def crear_libro(request):
    if request.method == 'POST':
        formulario = LibroForm(request.POST, request.FILES)  # Añadimos request.FILES para manejar archivos
        if formulario.is_valid():
            formulario.save()
            return redirect('lista_libros')
    else:
        formulario = LibroForm()
    
    return render(request, 'biblioteca/libro_form.html', {'formulario': formulario})

def detalle_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    alquiler_activo = None
    
    # Si el libro no está disponible, buscamos el alquiler actual
    if not libro.esta_disponible():
        alquiler_activo = Alquiler.objects.filter(libro=libro, estado='alquilado').last()
    
    return render(request, 'biblioteca/libro_detalle.html', {
        'libro': libro,
        'alquiler_activo': alquiler_activo
    })

@login_required
def editar_libro(request, pk):
    # SEGURIDAD: Solo el superusuario puede modificar libros. Si no es superusuario, lo redirigimos a la lista de libros.
    if not request.user.is_superuser:
        return redirect('lista_libros')

    libro = get_object_or_404(Libro, pk=pk)
    
    if request.method == 'POST':
        formulario = LibroForm(request.POST, request.FILES, instance=libro)
        if formulario.is_valid():
            formulario.save()
            return redirect('detalle_libro', pk=pk)
    else:
        formulario = LibroForm(instance=libro)
    
    return render(request, 'biblioteca/libro_form.html', {'formulario': formulario})
@login_required
def eliminar_libro(request, pk):
    # SEGURIDAD: Solo el superusuario puede eliminar libros. Si no es superusuario, lo redirigimos a la lista de libros.
    if not request.user.is_superuser:
        return redirect('lista_libros')
    libro = get_object_or_404(Libro, pk=pk)
    
    if request.method == 'POST':
        # Si confirma (le da al botón rojo), el libro se borra
        libro.delete()
        return redirect('lista_libros')
    
    # Si entra por primera vez, le mostramos la página de confirmación
    return render(request, 'biblioteca/libro_confirm_delete.html', {'libro': libro})

def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'biblioteca/autor_lista.html', {'autores': autores})

def detalle_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    return render(request, 'biblioteca/autor_detalle.html', {'autor': autor})

def editar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        formulario = AutorForm(request.POST, instance=autor)
        if formulario.is_valid():
            formulario.save()
            return redirect('detalle_autor', pk=pk)
    else:
        formulario = AutorForm(instance=autor)
    return render(request, 'biblioteca/autor_form.html', {'formulario': formulario})

def eliminar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == 'POST':
        autor.delete()
        return redirect('lista_autores')
    return render(request, 'biblioteca/autor_confirm_delete.html', {'autor': autor})

# --- GESTIÓN DE EDITORIALES ---

def lista_editoriales(request):
    editoriales = Editorial.objects.all()
    return render(request, 'biblioteca/editorial_lista.html', {'editoriales': editoriales})

def detalle_editorial(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    return render(request, 'biblioteca/editorial_detalle.html', {'editorial': editorial})

def editar_editorial(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    if request.method == 'POST':
        formulario = EditorialForm(request.POST, instance=editorial)
        if formulario.is_valid():
            formulario.save()
            return redirect('detalle_editorial', pk=pk)
    else:
        formulario = EditorialForm(instance=editorial)
    return render(request, 'biblioteca/editorial_form.html', {'formulario': formulario})

def eliminar_editorial(request, pk):
    editorial = get_object_or_404(Editorial, pk=pk)
    if request.method == 'POST':
        editorial.delete()
        return redirect('lista_editoriales')
    return render(request, 'biblioteca/editorial_confirm_delete.html', {'editorial': editorial})

class LibroListView(ListView):
    model = Libro
    template_name = 'biblioteca/lista_libros.html'
    context_object_name = 'libros'

@login_required
def alquilar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    
    # Si el libro ya está alquilado, no permitimos entrar aquí
    if not libro.esta_disponible():
        return redirect('lista_libros')

    # Calculamos la fecha de devolución (hoy + 15 días)
    fecha_devolucion = timezone.now() + timedelta(days=15)

    if request.method == 'POST':
        # Si el usuario confirma el alquiler (pulsa el botón del formulario)
        Alquiler.objects.create(
            usuario=request.user,
            libro=libro,
            fecha_devolucion_prevista=fecha_devolucion,
            estado='alquilado'
        )
        return redirect('mis_alquileres') # Llevamos al usuario a ver sus libros alquilados

    # Si es un GET (primera vez que entra), mostramos la página de confirmación
    return render(request, 'biblioteca/alquilar_confirmar.html', {
        'libro': libro,
        'fecha_devolucion': fecha_devolucion
    })

@login_required
def mis_alquileres(request):
    # Filtramos los alquileres del usuario actual, ordenados por fecha
    alquileres = Alquiler.objects.filter(usuario=request.user).order_by('-fecha_inicio')
    
    return render(request, 'biblioteca/mis_alquileres.html', {
        'alquileres': alquileres
    })
@login_required
def devolver_libro(request, pk):
    # Buscamos el alquiler que pertenezca al usuario actual
    alquiler = get_object_or_404(Alquiler, pk=pk, usuario=request.user)
    
    # Si el libro aún está alquilado, lo devolvemos
    if alquiler.estado == 'alquilado':
        alquiler.estado = 'devuelto'
        alquiler.fecha_devolucion_real = timezone.now()
        alquiler.save()
        
    return redirect('mis_alquileres')

@login_required
def toggle_disponibilidad(request, pk): #función para modificar la disponibilidad de un libro (alquilar o devolver) desde el detalle del libro. Solo para superusuario.
    # Seguridad estricta: Solo el superusuario puede usar esta función
    if not request.user.is_superuser:
        return redirect('lista_libros')

    libro = get_object_or_404(Libro, pk=pk)
    
    if libro.esta_disponible():
        # Lo marcamos como alquilado por el sistema
        Alquiler.objects.create(
            usuario=request.user,
            libro=libro,
            fecha_devolucion_prevista=timezone.now() + timedelta(days=15), 
            estado='alquilado'
        )
    else:
        # Buscamos el alquiler activo y lo cerramos
        alquiler_activo = Alquiler.objects.filter(libro=libro, estado='alquilado').last()
        if alquiler_activo:
            alquiler_activo.estado = 'devuelto'
            alquiler_activo.fecha_devolucion_real = timezone.now()
            alquiler_activo.save()

    return redirect('detalle_libro', pk=pk)

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario) # Logueamos al usuario automáticamente tras registrarse
            return redirect('lista_libros')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def gestion_alquileres(request):
        # Seguridad: solo el admin puede ver esta lista global
        if not request.user.is_superuser:
            return redirect('lista_libros')
        
        # Obtenemos solo los alquileres activos (no devueltos)
        alquileres_activos = Alquiler.objects.filter(estado='alquilado').order_by('fecha_devolucion_prevista')
        
        return render(request, 'biblioteca/gestion_alquileres.html', {
            'alquileres': alquileres_activos
        })