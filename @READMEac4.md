# Actividad 4 - Proyecto: modelar las interacciones entre los usuarios y los libros

**JORGE EDUARDO ROBLES NIÑO - 100199780**  
**08/11/2025**

**Corporación Universitaria Iberoamericana**  
**Ingeniería de Software**  
**Estructura de datos**

**JAVIER LUNA**

---

## Introducción

Este proyecto es de la segunda etapa del sistema de gestión de biblioteca desarrollado en la asignatura de Estructuras de Datos. Tras una primera versión basada en estructuras lineales (listas, colas y pilas) identifique la necesidad de mejorar la eficiencia de las operaciones más utilizadas en el programa como: registro, búsqueda y mantenimiento de usuarios y libros mediante estructuras no lineales. En particular, la adopción de árboles balanceados (AVL) permite mantener las colecciones ordenadas y garantizar tiempos de respuesta logarítmicos incluso frente a un crecimiento sostenido del catálogo y de los usuarios (Fritelli, 2017). Esta mejora impacta directamente en la experiencia de uso del sistema y en la escalabilidad de futuras funcionalidades.

---

## Desarrollo

### Modelo anterior y oportunidades de mejora

La versión inicial del sistema almacenaba usuarios y libros en listas simples. Aunque esta aproximación simplificaba la implementación, las operaciones de búsqueda y validación de duplicados requerían recorridos completos de las listas, con una complejidad O(n). Este enfoque generaba tiempos de respuesta crecientes a medida que aumentaba la cantidad de registros, especialmente visibles en los flujos de préstamo y devolución que consultan múltiples estructuras en secuencia. Entonces logramos identificar que las listas eran el principal cuello de botella para búsquedas por identificador único (ISBN o ID de usuario).

### Tipo de árbol seleccionado y justificación

Se optó por implementar árboles AVL para los catálogos de libros y usuarios. Los árboles AVL mantienen el balance de sus subárboles después de cada inserción o eliminación, conservando una altura O(log n) y, por ende, operaciones de búsqueda, inserción y borrado con complejidad logarítmica.
Esta propiedad resulta crucial para garantizar un rendimiento estable incluso con volúmenes de datos elevados. Además, la naturaleza numérica de las claves (ISBN e IDs) facilita la comparación y el mantenimiento del orden inherente requerido por un árbol binario de búsqueda balanceado. Las categorías se mantuvieron en lista debido a su frecuencia de consulta moderada y por no representar un cuello de botella crítico.

### Ejemplos de código

La integración del árbol AVL se materializó en un nuevo módulo arboles.py que define la estructura ArbolAVL y la clase NodoAVL. El árbol es parametrizable mediante una función que extrae la clave de cada entidad, lo que permite reutilizar la misma implementación para usuarios y libros:

```python
arboles.py :

class ArbolAVL:
    """
    Implementación de un Árbol AVL (balanceado) parametrizable por una función
    que a partir de cada elemento obtiene la clave de comparación.

    Se utiliza para almacenar entidades de la biblioteca y garantizar
    operaciones eficientes (O(log n)) incluso con altos volúmenes de datos.
    """

    def __init__(self, obtener_clave: Callable[[Any], Any]):
        self.raiz: Optional[NodoAVL] = None
        self.obtener_clave = obtener_clave
        self._tamaño = 0

    # =========================================================================
    # MÉTODOS PÚBLICOS
    # =========================================================================

    def insertar(self, valor: Any) -> bool:
        """
        Inserta un nuevo elemento en el árbol.
        Retorna True si se insertó un nuevo nodo, False si se actualizó un existente.
        """
        self.raiz, insertado = self._insertar(self.raiz, self.obtener_clave(valor), valor)
        if insertado:
            self._tamaño += 1
        return insertado

    def buscar(self, clave: Any) -> Optional[Any]:
        """Busca un elemento por su clave. Retorna el valor asociado o None si no existe."""
        nodo = self._buscar(self.raiz, clave)
        return nodo.valor if nodo else None

    def eliminar(self, clave: Any) -> bool:
        """
        Elimina el elemento con la clave indicada.
        Retorna True si el elemento existía y fue eliminado, False en caso contrario.
        """
        self.raiz, eliminado = self._eliminar(self.raiz, clave)
        if eliminado:
            self._tamaño -= 1
        return eliminado

    def recorrido_inorden(self) -> List[Any]:
        """Retorna una lista con los valores del árbol en orden ascendente por clave."""
        resultado: List[Any] = []
        self._inorden(self.raiz, resultado)
        return resultado

    def minimo(self) -> Optional[Any]:
        """Retorna el valor con clave mínima, o None si el árbol está vacío."""
        nodo = self._minimo(self.raiz)
        return nodo.valor if nodo else None

    def maximo(self) -> Optional[Any]:
        """Retorna el valor con clave máxima, o None si el árbol está vacío."""
        nodo = self._maximo(self.raiz)
        return nodo.valor if nodo else None

    def __len__(self) -> int:
        """Permite usar len(arbol) para obtener el número de elementos almacenados."""
        return self._tamaño

    def esta_vacio(self) -> bool:
        """Retorna True si el árbol no contiene elementos."""
        return self.raiz is None

    # =========================================================================
    # MÉTODOS PRIVADOS (RECURSIVOS)
    # =========================================================================

    def _insertar(self, nodo: Optional[NodoAVL], clave: Any, valor: Any) -> Tuple[NodoAVL, bool]:
        if nodo is None:
            return NodoAVL(clave, valor), True

        if clave < nodo.clave:
            nodo.izquierda, insertado = self._insertar(nodo.izquierda, clave, valor)
        elif clave > nodo.clave:
            nodo.derecha, insertado = self._insertar(nodo.derecha, clave, valor)
        else:
            nodo.valor = valor
            return nodo, False

        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        return self._balancear(nodo), insertado

    def _buscar(self, nodo: Optional[NodoAVL], clave: Any) -> Optional[NodoAVL]:
```

En main.py, la sustitución de listas por árboles se refleja en las operaciones clave del sistema:

```python
main.py :

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
```

### Operaciones implementadas

Para cada árbol se implementaron las operaciones fundamentales:

- Inserción (insertar): agrega un nuevo nodo y rebalancea el árbol pues, si es necesario.
- Búsqueda (buscar): localiza una entidad en O(log n) usando la clave definida.
- Eliminación (eliminar): retira nodos y ajusta el balance mediante rotaciones simples o dobles.
- Recorridos (recorrido_inorden): permite listar ordenadamente los elementos para reportes y visualizaciones.

Estas operaciones se validan a través de pruebas unitarias en test_sistema.py, donde se incorporó un nuevo caso específico para el árbol AVL y se adaptó el flujo completo del sistema a la nueva estructura por si el docente prefiere correr el script de test.

### Análisis de eficiencia

Se diseñó un experimento comparativo entre las búsquedas en listas y en árboles AVL. Utilizando un conjunto de 2,000 libros y 400 búsquedas (mitad existentes, mitad inexistentes), se midieron los tiempos de ejecución:

- Lista lineal: 0.014 segundos
- Árbol AVL: 0.00035 segundos
- Factor de mejora aproximado: 41 × más rápido

Este resultado evidencia que el cambio a estructuras balanceadas reduce significativamente la carga computacional al escalar el volumen de datos, alineándose con las ventajas teóricas de los árboles AVL.

---

## Conclusiones

Podemos decir que la migración de estructuras lineales a árboles AVL nos permitió optimizar de forma sustancial el rendimiento del sistema de gestión de biblioteca porque las operaciones críticas (registro, préstamo y devolución) se benefician de búsquedas y validaciones logarítmicas, lo que nos permite garantizar una experiencia mas fluida incluso con catálogos amplios. La implementación reforzó el entendimiento práctico de los árboles balanceados y de sus rotaciones, destacando la importancia de elegir estructuras de datos adecuadas para cada necesidad. Entre las principales dificultades se encontraron la correcta implementación de las rotaciones y la adaptación del código existente a la nueva API del arbol pero pues, las pruebas unitarias facilitaron la verificación de cada ajuste. En comparación con las estructuras lineales, los árboles AVL ofrecen un desempeño superior en colecciones dinámicas al mantener orden y balance automáticamente, aunque exigen mayor complejidad de implementación.

---

## Bibliografia

Fritelli, V. Guzman, A. & Tymoschuk, J. (2020). Algoritmos y estructuras de datos (2a. ed.). Jorge Sarmiento Editor - Universitas. (Págs. 311 - 341).

Joyanes Aguilar, L. (2020). Fundamentos de programación: algoritmos, estructura de datos y objetos. (Págs. 492- 518).


