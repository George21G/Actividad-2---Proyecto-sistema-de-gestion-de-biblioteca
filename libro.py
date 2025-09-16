"""
Clase Libro - Representa un libro en el sistema de biblioteca
Contiene toda la información del libro y su estado de disponibilidad
"""

class Libro:
    """
    Constructor de la clase Libro
    Inicializa un nuevo libro con su información básica y estado
    """
    def __init__(self, isbn, titulo, autor, categoria, estado="Disponible"):
        # ISBN: Código único internacional que identifica al libro
        self.isbn = isbn
        
        # Título del libro
        self.titulo = titulo
        
        # Autor del libro
        self.autor = autor
        
        # Categoría a la que pertenece el libro (objeto CategoriaLibro)
        self.categoria = categoria
        
        # Estado del libro: "Disponible" o "No Disponible"
        # Por defecto se inicializa como "Disponible"
        self.estado = estado
