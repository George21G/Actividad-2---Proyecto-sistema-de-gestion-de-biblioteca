# 📚 Sistema de Gestión de Biblioteca

## Descripción
Sistema de gestión de biblioteca implementado en Python que utiliza programación orientada a objetos y estructuras de datos (cola y pila) para manejar usuarios, libros, categorías, préstamos y devoluciones.

## 🏗️ Estructura del Proyecto

### Entidades Principales

#### 👤 Usuarios
- **Id**: Identificador único del usuario
- **Nombre**: Nombre del usuario
- **Apellido**: Apellido del usuario
- **Correo**: Correo electrónico del usuario

#### 📚 Categorías de Libros
- **Id**: Identificador único de la categoría
- **Nombre**: Nombre de la categoría

#### 📖 Libros
- **ISBN**: Código único del libro
- **Título**: Título del libro
- **Autor**: Autor del libro
- **Categoría**: Categoría a la que pertenece el libro
- **Estado**: Disponible / No Disponible

### Estructuras de Datos

#### 🔄 Préstamos
- **Cola de Préstamos**: Mantiene las solicitudes en orden de llegada (FIFO)

#### 📜 Historial
- **Pila de Historial**: Conserva las devoluciones y préstamos (LIFO)

## 📁 Archivos del Proyecto

- `main.py` - Archivo principal con el menú y lógica del sistema
- `usuario.py` - Clase Usuario con sus atributos y métodos
- `libro.py` - Clase Libro con sus atributos y métodos
- `categoria_libro.py` - Clase CategoriaLibro
- `estructuras_datos.py` - Implementación de ColaPrestamos y PilaHistorial
- `test_sistema.py` - Suite de pruebas automatizadas del sistema
- `.gitignore` - Archivos a ignorar en el control de versiones

## 🚀 Funcionalidades

1. **Agregar categoría** - Crear nuevas categorías de libros
2. **Agregar libro** - Añadir libros al catálogo con categoría
3. **Registrar usuario** - Registrar nuevos usuarios con datos completos
4. **Prestar libro** - Prestar libros a usuarios (usando cola)
5. **Devolver libro** - Devolver libros prestados (usando pila)
6. **Mostrar catálogo** - Ver todos los libros disponibles
7. **Mostrar usuarios** - Ver usuarios registrados
8. **Mostrar historial** - Ver historial de transacciones

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Programación Orientada a Objetos**
- **Estructuras de Datos**: Cola (deque) y Pila (list)
- **Manejo de fechas**: datetime

## 📋 Cómo Ejecutar

### Ejecutar el Sistema Principal
1. Asegúrate de tener Python 3.x instalado
2. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
3. Sigue las instrucciones del menú interactivo

### Ejecutar las Pruebas
Para validar que el sistema funciona correctamente:
```bash
python test_sistema.py
```

### Flujo Recomendado de Uso
1. **Agregar categoría** (opción 1) - Crear categorías de libros
2. **Agregar libro** (opción 2) - Añadir libros al catálogo
3. **Registrar usuario** (opción 3) - Registrar usuarios
4. **Prestar libro** (opción 4) - Prestar libros
5. **Mostrar historial** (opción 8) - Ver transacciones

## 🎯 Características Técnicas

- ✅ **Programación Orientada a Objetos** - Clases bien estructuradas
- ✅ **Estructuras de Datos** - Cola FIFO y Pila LIFO implementadas
- ✅ **Validaciones de entrada** - Verificación de datos del usuario
- ✅ **Manejo de errores** - Gestión de casos excepcionales
- ✅ **Interfaz de usuario amigable** - Menú interactivo con emojis
- ✅ **Seguimiento de transacciones** - Historial con fechas y horas
- ✅ **Código documentado** - Comentarios detallados en todo el código
- ✅ **Pruebas automatizadas** - Suite de pruebas para validar funcionalidad

## 📊 Estructura de Datos Implementadas

### Cola de Préstamos (FIFO)
- **Propósito**: Mantener solicitudes de préstamos en orden de llegada
- **Implementación**: `collections.deque`
- **Operaciones**: Agregar solicitudes, procesar siguiente, ver siguiente

### Pila de Historial (LIFO)
- **Propósito**: Conservar historial de transacciones
- **Implementación**: `list` con operaciones de pila
- **Operaciones**: Agregar transacciones, obtener última, ver historial completo
