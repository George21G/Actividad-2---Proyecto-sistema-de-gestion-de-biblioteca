"""
Sistema de Gestión de Biblioteca - Archivo Principal
Contiene la lógica principal del sistema y el menú interactivo
"""

# Importar todas las clases necesarias del sistema
from libro import Libro
from usuario import Usuario
from categoria_libro import CategoriaLibro
from estructuras_datos import ColaPrestamos, PilaHistorial
from arboles import ArbolAVL

# =============================================================================
# VARIABLES GLOBALES DEL SISTEMA
# =============================================================================

# Árboles principales que almacenan los datos del sistema
arbol_libros = ArbolAVL(lambda libro: libro.isbn)           # Libros del catálogo
arbol_usuarios = ArbolAVL(lambda usuario: usuario.id_usuario)  # Usuarios registrados
lista_categorias = []    # Categorías de libros (se mantienen en lista)

# Estructuras de datos para manejar transacciones
cola_prestamos = ColaPrestamos()    # Cola FIFO para solicitudes de préstamos
pila_historial = PilaHistorial()    # Pila LIFO para historial de transacciones

# =============================================================================
# FUNCIONES DE GESTIÓN DE CATEGORÍAS
# =============================================================================

def agregar_categoria():
    """
    Función para agregar una nueva categoría de libros al sistema
    Solicita al usuario el ID y nombre de la categoría
    """
    # Solicitar información de la categoría al usuario
    id_categoria = input("ID de la categoría: ")
    nombre = input("Nombre de la categoría: ")
    
    # Validar que no exista ya la categoría
    if any(cat.id_categoria == id_categoria for cat in lista_categorias):
        print("❌ Ya existe una categoría con ese ID.")
        return

    # Crear objeto CategoriaLibro con los datos ingresados
    categoria = CategoriaLibro(id_categoria, nombre)

    # Agregar la categoría a la lista global de categorías
    lista_categorias.append(categoria)

    # Confirmar al usuario que la categoría fue agregada
    print("✅ Categoría agregada.")

# =============================================================================
# FUNCIONES DE GESTIÓN DE LIBROS
# =============================================================================

def agregar_libro():
    """
    Función para agregar un nuevo libro al catálogo
    Solicita información del libro y permite seleccionar una categoría existente
    """
    # Solicitar información básica del libro
    isbn = input("ISBN del libro: ")
    titulo = input("Título del libro: ")
    autor = input("Autor: ")
    
    # Verificar que existan categorías disponibles
    if not lista_categorias:
        print("❌ No hay categorías disponibles. Agrega una categoría primero.")
        return
    
    # Mostrar categorías disponibles para que el usuario seleccione
    print("\nCategorías disponibles:")
    for i, cat in enumerate(lista_categorias):
        print(f"{i+1}. {cat.nombre} (ID: {cat.id_categoria})")
    
    try:
        # Solicitar al usuario que seleccione una categoría
        opcion = int(input("Selecciona el número de la categoría: ")) - 1
        
        # Validar que la opción seleccionada sea válida
        if 0 <= opcion < len(lista_categorias):
            categoria = lista_categorias[opcion]  # Obtener la categoría seleccionada
            
            if arbol_libros.buscar(isbn):
                print("❌ Ya existe un libro con ese ISBN.")
                return

            # Crear objeto Libro con todos los datos
            libro = Libro(isbn, titulo, autor, categoria)

            # Agregar el libro al árbol global de libros
            arbol_libros.insertar(libro)

            # Confirmar al usuario que el libro fue agregado
            print("✅ Libro agregado.")
        else:
            print("❌ Opción inválida.")
    except ValueError:
        # Manejar error si el usuario no ingresa un número válido
        print("❌ Por favor ingresa un número válido.")

# =============================================================================
# FUNCIONES DE GESTIÓN DE USUARIOS
# =============================================================================

def registrar_usuario():
    """
    Función para registrar un nuevo usuario en el sistema
    Solicita todos los datos personales del usuario
    """
    # Solicitar información personal del usuario
    id_usuario = input("ID del usuario: ")
    nombre = input("Nombre del usuario: ")
    apellido = input("Apellido del usuario: ")
    correo = input("Correo del usuario: ")
    
    if arbol_usuarios.buscar(id_usuario):
        print("❌ Ya existe un usuario con ese ID.")
        return

    # Crear objeto Usuario con todos los datos ingresados
    usuario = Usuario(id_usuario, nombre, apellido, correo)

    # Agregar el usuario al árbol global de usuarios
    arbol_usuarios.insertar(usuario)

    # Confirmar al usuario que el registro fue exitoso
    print("✅ Usuario registrado.")

# =============================================================================
# FUNCIONES DE GESTIÓN DE PRÉSTAMOS Y DEVOLUCIONES
# =============================================================================

def prestar_libro():
    """
    Función para prestar un libro a un usuario
    Valida que el usuario y libro existan, y que el libro esté disponible
    """
    # Solicitar información para el préstamo
    id_usuario = input("ID del usuario: ")
    isbn = input("ISBN del libro: ")

    # Buscar el libro por ISBN en el árbol de libros
    libro = arbol_libros.buscar(isbn)

    # Buscar el usuario por ID en el árbol de usuarios
    usuario = arbol_usuarios.buscar(id_usuario)

    # Verificar que tanto el libro como el usuario existan
    if libro and usuario:
        # Verificar que el libro esté disponible para préstamo
        if libro.estado == "Disponible":
            # Cambiar el estado del libro a "No Disponible"
            libro.estado = "No Disponible"
            
            # Agregar el libro a la lista de libros prestados del usuario
            usuario.libros_prestados.append(libro)
            
            # Agregar la solicitud a la cola de préstamos (FIFO)
            cola_prestamos.agregar_solicitud(id_usuario, isbn)
            
            # Agregar la transacción al historial (pila LIFO)
            pila_historial.agregar_transaccion('prestamo', id_usuario, isbn)
            
            # Confirmar el préstamo exitoso
            print("📚 Libro prestado.")
        else:
            print("❌ Libro no disponible.")
    else:
        print("❌ Usuario o libro no encontrado.")

def devolver_libro():
    """
    Función para devolver un libro prestado
    Valida que el usuario exista y tenga el libro prestado
    """
    # Solicitar información para la devolución
    id_usuario = input("ID del usuario: ")
    isbn = input("ISBN del libro: ")

    # Buscar el usuario por ID en el árbol de usuarios
    usuario = arbol_usuarios.buscar(id_usuario)

    # Verificar que el usuario exista
    if usuario:
        # Buscar el libro en la lista de libros prestados del usuario
        libro = next((l for l in usuario.libros_prestados if l.isbn == isbn), None)
        
        # Verificar que el usuario tenga ese libro prestado
        if libro:
            # Cambiar el estado del libro a "Disponible"
            libro.estado = "Disponible"
            
            # Remover el libro de la lista de libros prestados del usuario
            usuario.libros_prestados.remove(libro)
            
            # Agregar la transacción de devolución al historial (pila LIFO)
            pila_historial.agregar_transaccion('devolucion', id_usuario, isbn)
            
            # Confirmar la devolución exitosa
            print("🔁 Libro devuelto.")
        else:
            print("❌ El usuario no tiene ese libro.")
    else:
        print("❌ Usuario no encontrado.")

# =============================================================================
# FUNCIONES DE VISUALIZACIÓN Y CONSULTA
# =============================================================================

def mostrar_catalogo():
    """
    Función para mostrar todos los libros del catálogo
    Muestra información completa de cada libro incluyendo su estado
    """
    # Verificar si hay libros en el catálogo
    if arbol_libros.esta_vacio():
        print("📚 No hay libros en el catálogo.")
        return
    
    # Mostrar encabezado del catálogo
    print("\n📚 CATÁLOGO DE LIBROS 📚")
    
    # Iterar sobre todos los libros y mostrar su información
    for libro in arbol_libros.recorrido_inorden():
        print(f"ISBN: {libro.isbn}")
        print(f"Título: {libro.titulo}")
        print(f"Autor: {libro.autor}")
        print(f"Categoría: {libro.categoria.nombre}")
        print(f"Estado: {libro.estado}")
        print("-" * 40)  # Línea separadora entre libros

def mostrar_usuarios():
    """
    Función para mostrar todos los usuarios registrados en el sistema
    Muestra información personal y cantidad de libros prestados
    """
    # Verificar si hay usuarios registrados
    if arbol_usuarios.esta_vacio():
        print("👥 No hay usuarios registrados.")
        return
    
    # Mostrar encabezado de usuarios
    print("\n👥 USUARIOS REGISTRADOS 👥")
    
    # Iterar sobre todos los usuarios y mostrar su información
    for usuario in arbol_usuarios.recorrido_inorden():
        print(f"ID: {usuario.id_usuario}")
        print(f"Nombre: {usuario.nombre} {usuario.apellido}")
        print(f"Correo: {usuario.correo}")
        print(f"Libros prestados: {len(usuario.libros_prestados)}")
        print("-" * 40)  # Línea separadora entre usuarios

def mostrar_historial():
    """
    Función para mostrar el historial completo de transacciones
    Muestra todas las transacciones de préstamos y devoluciones con fechas
    """
    # Obtener una copia del historial completo sin modificar la pila original
    historial = pila_historial.obtener_historial_completo()
    
    # Verificar si hay transacciones en el historial
    if not historial:
        print("📜 No hay transacciones en el historial.")
        return
    
    # Mostrar encabezado del historial
    print("\n📜 HISTORIAL DE TRANSACCIONES 📜")
    
    # Iterar sobre todas las transacciones y mostrar su información
    for transaccion in historial:
        print(f"Tipo: {transaccion['tipo'].upper()}")  # Convertir a mayúsculas para mejor visualización
        print(f"Usuario ID: {transaccion['id_usuario']}")
        print(f"ISBN: {transaccion['isbn']}")
        print(f"Fecha: {transaccion['fecha_transaccion']}")
        print("-" * 40)  # Línea separadora entre transacciones

# =============================================================================
# FUNCIÓN PRINCIPAL DEL SISTEMA - MENÚ INTERACTIVO
# =============================================================================

def menu():
    """
    Función principal que maneja el menú interactivo del sistema
    Permite al usuario navegar por todas las funcionalidades disponibles
    """
    # Bucle infinito para mantener el menú activo hasta que el usuario decida salir
    while True:
        # Mostrar el menú principal con todas las opciones disponibles
        print("\n📚 MENU BIBLIOTECA 📚")
        print("1. Agregar categoría")
        print("2. Agregar libro")
        print("3. Registrar usuario")
        print("4. Prestar libro")
        print("5. Devolver libro")
        print("6. Mostrar catálogo")
        print("7. Mostrar usuarios")
        print("8. Mostrar historial")
        print("9. Salir")
        
        # Solicitar al usuario que elija una opción
        opcion = input("Elige una opción: ")

        # Procesar la opción seleccionada por el usuario
        if opcion == "1":
            agregar_categoria()      # Llamar función para agregar categoría
        elif opcion == "2":
            agregar_libro()          # Llamar función para agregar libro
        elif opcion == "3":
            registrar_usuario()      # Llamar función para registrar usuario
        elif opcion == "4":
            prestar_libro()          # Llamar función para prestar libro
        elif opcion == "5":
            devolver_libro()         # Llamar función para devolver libro
        elif opcion == "6":
            mostrar_catalogo()       # Llamar función para mostrar catálogo
        elif opcion == "7":
            mostrar_usuarios()       # Llamar función para mostrar usuarios
        elif opcion == "8":
            mostrar_historial()      # Llamar función para mostrar historial
        elif opcion == "9":
            print("👋 Saliendo del sistema...")
            break  # Salir del bucle y terminar el programa
        else:
            print("❗ Opción inválida.")  # Mostrar mensaje de error para opciones inválidas

# =============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =============================================================================

# Iniciar el menú principal cuando se ejecute el archivo
if __name__ == "__main__":
    menu()