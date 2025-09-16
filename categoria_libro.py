"""
Clase CategoriaLibro - Representa una categoría de libros en el sistema
Permite clasificar los libros por temas o géneros
"""

class CategoriaLibro:
    """
    Constructor de la clase CategoriaLibro
    Inicializa una nueva categoría con su identificador y nombre
    """
    def __init__(self, id_categoria, nombre):
        # Identificador único de la categoría en el sistema
        self.id_categoria = id_categoria
        
        # Nombre descriptivo de la categoría (ej: "Ficción", "Ciencia", "Historia")
        self.nombre = nombre

