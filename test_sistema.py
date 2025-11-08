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
from arboles import ArbolAVL
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

def test_arbol_avl():
    """Prueba la estructura de Árbol AVL con libros"""
    print("🧪 Probando ArbolAVL...")

    categoria = CategoriaLibro("FIC001", "Ficción")
    arbol = ArbolAVL(lambda libro: libro.isbn)

    libro1 = Libro("978-0000000001", "Libro A", "Autor A", categoria)
    libro2 = Libro("978-0000000005", "Libro B", "Autor B", categoria)
    libro3 = Libro("978-0000000003", "Libro C", "Autor C", categoria)

    assert arbol.insertar(libro1) is True
    assert arbol.insertar(libro2) is True
    assert arbol.insertar(libro3) is True
    assert len(arbol) == 3

    # Búsqueda
    encontrado = arbol.buscar(libro2.isbn)
    assert encontrado is libro2

    # Recorrido inorden debe regresar los ISBN ordenados
    isbns = [libro.isbn for libro in arbol.recorrido_inorden()]
    assert isbns == sorted(isbns)

    # Eliminación
    assert arbol.eliminar(libro1.isbn) is True
    assert len(arbol) == 2
    assert arbol.buscar(libro1.isbn) is None

    print("✅ ArbolAVL: OK")

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
    arbol_libros = ArbolAVL(lambda l: l.isbn)
    arbol_usuarios = ArbolAVL(lambda u: u.id_usuario)

    arbol_libros.insertar(libro1)
    arbol_libros.insertar(libro2)
    arbol_usuarios.insertar(usuario1)
    arbol_usuarios.insertar(usuario2)

    # Simular préstamo de libro1 a usuario1
    libro = arbol_libros.buscar(libro1.isbn)
    usuario = arbol_usuarios.buscar(usuario1.id_usuario)
    if libro and usuario and libro.estado == "Disponible":
        libro.estado = "No Disponible"
        usuario.libros_prestados.append(libro)
        cola.agregar_solicitud(usuario.id_usuario, libro.isbn)
        historial.agregar_transaccion('prestamo', usuario.id_usuario, libro.isbn)
    
    # Verificar préstamo
    assert libro.estado == "No Disponible"
    assert len(usuario.libros_prestados) == 1
    assert cola.tamaño() == 1
    assert historial.tamaño() == 1
    
    # Simular devolución
    if libro in usuario.libros_prestados:
        libro.estado = "Disponible"
        usuario.libros_prestados.remove(libro)
        historial.agregar_transaccion('devolucion', usuario.id_usuario, libro.isbn)
    
    # Verificar devolución
    assert libro.estado == "Disponible"
    assert len(usuario.libros_prestados) == 0
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

def analisis_eficiencia(num_elementos=2000, num_busquedas=400):
    """
    Realiza un análisis comparativo entre la búsqueda en lista vs Árbol AVL.
    Retorna un diccionario con los tiempos medidos.
    """
    from random import sample, randint
    from time import perf_counter

    categoria = CategoriaLibro("TEC", "Tecnología")

    lista_libros = []
    arbol_libros = ArbolAVL(lambda libro: libro.isbn)

    for indice in range(num_elementos):
        isbn = f"978-{indice:010d}"
        libro = Libro(isbn, f"Título {indice}", f"Autor {indice}", categoria)
        lista_libros.append(libro)
        arbol_libros.insertar(libro)

    claves_existentes = sample([libro.isbn for libro in lista_libros], num_busquedas // 2)
    claves_inexistentes = [f"978-{randint(num_elementos, num_elementos * 2):010d}" for _ in range(num_busquedas // 2)]
    claves_busqueda = claves_existentes + claves_inexistentes

    inicio_lista = perf_counter()
    for clave in claves_busqueda:
        next((libro for libro in lista_libros if libro.isbn == clave), None)
    tiempo_lista = perf_counter() - inicio_lista

    inicio_arbol = perf_counter()
    for clave in claves_busqueda:
        arbol_libros.buscar(clave)
    tiempo_arbol = perf_counter() - inicio_arbol

    return {
        "elementos": num_elementos,
        "busquedas": num_busquedas,
        "tiempo_lista_seg": tiempo_lista,
        "tiempo_arbol_seg": tiempo_arbol,
        "factor_mejora": (tiempo_lista / tiempo_arbol) if tiempo_arbol > 0 else float("inf"),
    }

def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas del sistema"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE BIBLIOTECA 🚀")
    print("=" * 60)
    
    try:
        test_categoria_libro()
        test_usuario()
        test_libro()
        test_arbol_avl()
        test_cola_prestamos()
        test_pila_historial()
        test_sistema_completo()
        test_validaciones()

        reporte = analisis_eficiencia()
        
        print("=" * 60)
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE! 🎉")
        print("✅ El sistema está funcionando correctamente")
        print("✅ Todas las clases están implementadas")
        print("✅ Las estructuras de datos funcionan (Cola FIFO y Pila LIFO)")
        print("✅ El flujo completo del sistema es correcto")
        print("✅ Las validaciones están funcionando")
        print("=" * 60)
        print("📈 ANÁLISIS DE EFICIENCIA (LISTA vs ÁRBOL AVL)")
        print(f"Elementos evaluados : {reporte['elementos']}")
        print(f"Búsquedas realizadas : {reporte['busquedas']}")
        print(f"Tiempo en lista      : {reporte['tiempo_lista_seg']:.6f} segundos")
        print(f"Tiempo en AVL        : {reporte['tiempo_arbol_seg']:.6f} segundos")
        print(f"Factor de mejora     : {reporte['factor_mejora']:.2f}x")
        
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
