"""
Módulo de Estructuras de Datos - Implementa Cola y Pila para el sistema de biblioteca
Contiene las clases ColaPrestamos y PilaHistorial que manejan las transacciones
"""

from collections import deque  # Importa deque para implementar cola eficientemente
from datetime import datetime  # Importa datetime para manejar fechas

class ColaPrestamos:
    """
    Cola que mantiene las solicitudes de préstamos en orden de llegada (FIFO)
    First In, First Out - El primero en llegar es el primero en ser atendido
    """
    def __init__(self):
        # Inicializa la cola usando deque (double-ended queue) para eficiencia
        self.cola = deque()
    
    def agregar_solicitud(self, id_usuario, isbn, fecha_solicitud=None):
        """
        Agrega una nueva solicitud de préstamo al final de la cola
        Si no se proporciona fecha, usa la fecha y hora actual
        """
        # Si no se proporciona fecha, usar la fecha y hora actual
        if fecha_solicitud is None:
            fecha_solicitud = datetime.now()
        
        # Crear diccionario con la información de la solicitud
        solicitud = {
            'id_usuario': id_usuario,      # ID del usuario que solicita
            'isbn': isbn,                  # ISBN del libro solicitado
            'fecha_solicitud': fecha_solicitud  # Fecha y hora de la solicitud
        }
        
        # Agregar la solicitud al final de la cola
        self.cola.append(solicitud)
    
    def procesar_siguiente(self):
        """
        Procesa la siguiente solicitud en la cola (FIFO)
        Remueve y retorna la primera solicitud de la cola
        """
        if self.cola:
            # popleft() remueve y retorna el primer elemento (FIFO)
            return self.cola.popleft()
        return None  # Retorna None si la cola está vacía
    
    def ver_siguiente(self):
        """
        Ve la siguiente solicitud sin removerla de la cola
        Útil para consultar sin procesar
        """
        if self.cola:
            # Retorna el primer elemento sin removerlo
            return self.cola[0]
        return None  # Retorna None si la cola está vacía
    
    def esta_vacia(self):
        """Verifica si la cola está vacía"""
        return len(self.cola) == 0
    
    def tamaño(self):
        """Retorna el número de solicitudes en la cola"""
        return len(self.cola)

class PilaHistorial:
    """
    Pila que conserva las devoluciones y préstamos (LIFO)
    Last In, First Out - El último en entrar es el primero en salir
    Útil para mantener un historial de transacciones
    """
    def __init__(self):
        # Inicializa la pila como una lista vacía
        self.pila = []
    
    def agregar_transaccion(self, tipo, id_usuario, isbn, fecha_transaccion=None):
        """
        Agrega una transacción al historial
        Las transacciones se agregan al final de la pila
        """
        # Si no se proporciona fecha, usar la fecha y hora actual
        if fecha_transaccion is None:
            fecha_transaccion = datetime.now()
        
        # Crear diccionario con la información de la transacción
        transaccion = {
            'tipo': tipo,                    # Tipo: 'prestamo' o 'devolucion'
            'id_usuario': id_usuario,        # ID del usuario involucrado
            'isbn': isbn,                    # ISBN del libro
            'fecha_transaccion': fecha_transaccion  # Fecha y hora de la transacción
        }
        
        # Agregar la transacción al final de la pila
        self.pila.append(transaccion)
    
    def ver_ultima_transaccion(self):
        """
        Ve la última transacción sin removerla de la pila
        Útil para consultar la transacción más reciente
        """
        if self.pila:
            # Retorna el último elemento sin removerlo
            return self.pila[-1]
        return None  # Retorna None si la pila está vacía
    
    def obtener_ultima_transaccion(self):
        """
        Obtiene y remueve la última transacción (LIFO)
        Útil para procesar transacciones en orden inverso
        """
        if self.pila:
            # pop() remueve y retorna el último elemento (LIFO)
            return self.pila.pop()
        return None  # Retorna None si la pila está vacía
    
    def esta_vacia(self):
        """Verifica si la pila está vacía"""
        return len(self.pila) == 0
    
    def tamaño(self):
        """Retorna el número de transacciones en la pila"""
        return len(self.pila)
    
    def obtener_historial_completo(self):
        """
        Obtiene todo el historial sin removerlo
        Retorna una copia de la pila para no modificar el original
        """
        return self.pila.copy()

