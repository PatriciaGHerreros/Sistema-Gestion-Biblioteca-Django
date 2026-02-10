from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.lista_libros, name='lista_libros'),
    
    # Autor 
    path('autor/nuevo/', views.crear_autor, name='crear_autor'),
    
    # Editorial 
    path('editorial/nueva/', views.crear_editorial, name='crear_editorial'),
    
    # Libro 
    path('libro/nuevo/', views.crear_libro, name='crear_libro'),

    # Detalle del libro 
    path('libro/<int:pk>/', views.detalle_libro, name='detalle_libro'),
    
    # Editar libro
    path('libro/<int:pk>/editar/', views.editar_libro, name='editar_libro'),

    # Eliminar libro
    path('libro/<int:pk>/eliminar/', views.eliminar_libro, name='eliminar_libro'),

    # Lista de autores
    path('autores/', views.lista_autores, name='lista_autores'),

    # Detalle del autor
    path('autor/<int:pk>/', views.detalle_autor, name='detalle_autor'),

    # Editar autor
    path('autor/<int:pk>/editar/', views.editar_autor, name='editar_autor'),
    
    # Eliminar autor
    path('autor/<int:pk>/eliminar/', views.eliminar_autor, name='eliminar_autor'),

    # Rutas para Editoriales
    path('editoriales/', views.lista_editoriales, name='lista_editoriales'),
    path('editorial/<int:pk>/', views.detalle_editorial, name='detalle_editorial'),
    path('editorial/<int:pk>/editar/', views.editar_editorial, name='editar_editorial'),
    path('editorial/<int:pk>/eliminar/', views.eliminar_editorial, name='eliminar_editorial'),
    path('libro/<int:pk>/alquilar/', views.alquilar_libro, name='alquilar_libro'),
    path('mis-alquileres/', views.mis_alquileres, name='mis_alquileres'),
    path('alquiler/<int:pk>/devolver/', views.devolver_libro, name='devolver_libro'),
    path('libro/<int:pk>/toggle-disponibilidad/', views.toggle_disponibilidad, name='toggle_disponibilidad'),
    path('registro/', views.registro, name='registro'),
    path('gestion/alquileres/', views.gestion_alquileres, name='gestion_alquileres'),

]