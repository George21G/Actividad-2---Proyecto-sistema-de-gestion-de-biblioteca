"""
Clase Usuario - Representa a un usuario del sistema de biblioteca
Contiene toda la información personal del usuario y los libros que tiene prestados
"""

class Usuario:
    """
    Constructor de la clase Usuario
    Inicializa un nuevo usuario con sus datos personales
    """
    def __init__(self, id_usuario, nombre, apellido, correo):
        # Identificador único del usuario en el sistema
        self.id_usuario = id_usuario
        
        # Nombre del usuario
        self.nombre = nombre
        
        # Apellido del usuario
        self.apellido = apellido
        
        # Correo electrónico del usuario
        self.correo = correo
        
        # Lista que almacena los libros que el usuario tiene prestados actualmente
        # Se inicializa como lista vacía
        self.libros_prestados = []