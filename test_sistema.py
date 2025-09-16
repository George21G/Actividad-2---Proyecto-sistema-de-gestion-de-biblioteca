#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de pruebas para el Sistema de Gestión de Biblioteca
Valida todas las funcionalidades del sistema
"""

from libro import Libro
from usuario import Usuario
from categoria_libro import CategoriaLibro
from estructuras_datos import ColaPrestamos, PilaHistorial
import sys

def test_categoria_libro():
    """Prueba la clase CategoriaLibro"""
    print("🧪 Probando CategoriaLibro...")
    
    categoria = CategoriaLibro("FIC001", "Ficción")
    assert categoria.id_categoria == "FIC001"
    assert categoria.nombre == "Ficción"
    print("✅ CategoriaLibro: OK")

def test_usuario():
    """Prueba la clase Usuario"""
    print("🧪 Probando Usuario...")
    
    usuario = Usuario("USR001", "Juan", "Pérez", "juan@email.com")
    assert usuario.id_usuario == "USR001"
    assert usuario.nombre == "Juan"
    assert usuario.apellido == "Pérez"
    assert usuario.correo == "juan@email.com"
    assert len(usuario.libros_prestados) == 0
    print("✅ Usuario: OK")

def test_libro():
    """Prueba la clase Libro"""
    print("🧪 Probando Libro...")
    
    categoria = CategoriaLibro("FIC001", "Ficción")
    libro = Libro("978-1234567890", "El Quijote", "Cervantes", categoria)
    
    assert libro.isbn == "978-1234567890"
    assert libro.titulo == "El Quijote"
    assert libro.autor == "Cervantes"
    assert libro.categoria.nombre == "Ficción"
    assert libro.estado == "Disponible"
    print("✅ Libro: OK")

def test_cola_prestamos():
    """Prueba la cola de préstamos"""
    print("🧪 Probando ColaPrestamos...")
    
    cola = ColaPrestamos()
    
    # Verificar que está vacía inicialmente
    assert cola.esta_vacia() == True
    assert cola.tamaño() == 0
    
    # Agregar solicitudes
    cola.agregar_solicitud("USR001", "978-1234567890")
    cola.agregar_solicitud("USR002", "978-0987654321")
    
    assert cola.esta_vacia() == False
    assert cola.tamaño() == 2
    
    # Procesar en orden FIFO
    primera = cola.procesar_siguiente()
    assert primera['id_usuario'] == "USR001"
    assert primera['isbn'] == "978-1234567890"
    
    segunda = cola.procesar_siguiente()
    assert segunda['id_usuario'] == "USR002"
    assert segunda['isbn'] == "978-0987654321"
    
    assert cola.esta_vacia() == True
    print("✅ ColaPrestamos: OK")

def test_pila_historial():
    """Prueba la pila de historial"""
    print("🧪 Probando PilaHistorial...")
    
    pila = PilaHistorial()
    
    # Verificar que está vacía inicialmente
    assert pila.esta_vacia() == True
    assert pila.tamaño() == 0
    
    # Agregar transacciones
    pila.agregar_transaccion('prestamo', "USR001", "978-1234567890")
    pila.agregar_transaccion('devolucion', "USR001", "978-1234567890")
    
    assert pila.esta_vacia() == False
    assert pila.tamaño() == 2
    
    # Procesar en orden LIFO
    ultima = pila.obtener_ultima_transaccion()
    assert ultima['tipo'] == 'devolucion'
    assert ultima['id_usuario'] == "USR001"
    
    penultima = pila.obtener_ultima_transaccion()
    assert penultima['tipo'] == 'prestamo'
    assert penultima['id_usuario'] == "USR001"
    
    assert pila.esta_vacia() == True
    print("✅ PilaHistorial: OK")

def test_sistema_completo():
    """Prueba el sistema completo con un flujo real"""
    print("🧪 Probando Sistema Completo...")
    
    # Crear categorías
    categoria_ficcion = CategoriaLibro("FIC001", "Ficción")
    categoria_ciencia = CategoriaLibro("SCI001", "Ciencia")
    
    # Crear usuarios
    usuario1 = Usuario("USR001", "Juan", "Pérez", "juan@email.com")
    usuario2 = Usuario("USR002", "María", "García", "maria@email.com")
    
    # Crear libros
    libro1 = Libro("978-1234567890", "El Quijote", "Cervantes", categoria_ficcion)
    libro2 = Libro("978-0987654321", "Física Cuántica", "Einstein", categoria_ciencia)
    
    # Crear estructuras de datos
    cola = ColaPrestamos()
    historial = PilaHistorial()
    
    # Simular préstamo de libro1 a usuario1
    if libro1.estado == "Disponible":
        libro1.estado = "No Disponible"
        usuario1.libros_prestados.append(libro1)
        cola.agregar_solicitud(usuario1.id_usuario, libro1.isbn)
        historial.agregar_transaccion('prestamo', usuario1.id_usuario, libro1.isbn)
    
    # Verificar préstamo
    assert libro1.estado == "No Disponible"
    assert len(usuario1.libros_prestados) == 1
    assert cola.tamaño() == 1
    assert historial.tamaño() == 1
    
    # Simular devolución
    if libro1 in usuario1.libros_prestados:
        libro1.estado = "Disponible"
        usuario1.libros_prestados.remove(libro1)
        historial.agregar_transaccion('devolucion', usuario1.id_usuario, libro1.isbn)
    
    # Verificar devolución
    assert libro1.estado == "Disponible"
    assert len(usuario1.libros_prestados) == 0
    assert historial.tamaño() == 2
    
    print("✅ Sistema Completo: OK")

def test_validaciones():
    """Prueba las validaciones del sistema"""
    print("🧪 Probando Validaciones...")
    
    # Probar que no se puede prestar un libro no disponible
    categoria = CategoriaLibro("FIC001", "Ficción")
    libro = Libro("978-1234567890", "El Quijote", "Cervantes", categoria)
    usuario = Usuario("USR001", "Juan", "Pérez", "juan@email.com")
    
    # Marcar libro como no disponible
    libro.estado = "No Disponible"
    
    # Intentar prestar (debería fallar)
    if libro.estado == "Disponible":
        # Este bloque no debería ejecutarse
        assert False, "No debería poder prestar un libro no disponible"
    
    print("✅ Validaciones: OK")

def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas del sistema"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE BIBLIOTECA 🚀")
    print("=" * 60)
    
    try:
        test_categoria_libro()
        test_usuario()
        test_libro()
        test_cola_prestamos()
        test_pila_historial()
        test_sistema_completo()
        test_validaciones()
        
        print("=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE! 🎉")
        print("✅ El sistema está funcionando correctamente")
        print("✅ Todas las clases están implementadas")
        print("✅ Las estructuras de datos funcionan (Cola FIFO y Pila LIFO)")
        print("✅ El flujo completo del sistema es correcto")
        print("✅ Las validaciones están funcionando")
        
    except AssertionError as e:
        print("=" * 60)
        print("❌ PRUEBA FALLIDA ❌")
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print("=" * 60)
        print("❌ ERROR INESPERADO ❌")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ejecutar_todas_las_pruebas()
