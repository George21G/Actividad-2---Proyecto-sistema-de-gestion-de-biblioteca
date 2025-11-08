"""
Módulo de Árboles para el Sistema de Biblioteca
Implementa un Árbol AVL genérico para mejorar las operaciones de búsqueda,
inserción y eliminación de entidades como libros y usuarios.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, List, Tuple


@dataclass
class NodoAVL:
    """Nodo del Árbol AVL que almacena una llave y el valor asociado."""

    clave: Any
    valor: Any
    izquierda: Optional["NodoAVL"] = None
    derecha: Optional["NodoAVL"] = None
    altura: int = 1


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
        if nodo is None:
            return None
        if clave == nodo.clave:
            return nodo
        if clave < nodo.clave:
            return self._buscar(nodo.izquierda, clave)
        return self._buscar(nodo.derecha, clave)

    def _eliminar(self, nodo: Optional[NodoAVL], clave: Any) -> Tuple[Optional[NodoAVL], bool]:
        if nodo is None:
            return None, False

        if clave < nodo.clave:
            nodo.izquierda, eliminado = self._eliminar(nodo.izquierda, clave)
        elif clave > nodo.clave:
            nodo.derecha, eliminado = self._eliminar(nodo.derecha, clave)
        else:
            eliminado = True
            if nodo.izquierda is None:
                return nodo.derecha, True
            if nodo.derecha is None:
                return nodo.izquierda, True
            sucesor = self._minimo(nodo.derecha)
            nodo.clave = sucesor.clave
            nodo.valor = sucesor.valor
            nodo.derecha, _ = self._eliminar(nodo.derecha, sucesor.clave)

        if nodo is None:
            return None, eliminado

        nodo.altura = 1 + max(self._altura(nodo.izquierda), self._altura(nodo.derecha))
        return self._balancear(nodo), eliminado

    def _inorden(self, nodo: Optional[NodoAVL], resultado: List[Any]) -> None:
        if nodo is None:
            return
        self._inorden(nodo.izquierda, resultado)
        resultado.append(nodo.valor)
        self._inorden(nodo.derecha, resultado)

    # =========================================================================
    # MÉTODOS DE BALANCEO
    # =========================================================================

    @staticmethod
    def _altura(nodo: Optional[NodoAVL]) -> int:
        return nodo.altura if nodo else 0

    def _factor_balance(self, nodo: Optional[NodoAVL]) -> int:
        if nodo is None:
            return 0
        return self._altura(nodo.izquierda) - self._altura(nodo.derecha)

    def _balancear(self, nodo: NodoAVL) -> NodoAVL:
        balance = self._factor_balance(nodo)

        # Caso Izquierda-Izquierda
        if balance > 1 and self._factor_balance(nodo.izquierda) >= 0:
            return self._rotacion_derecha(nodo)

        # Caso Izquierda-Derecha
        if balance > 1 and self._factor_balance(nodo.izquierda) < 0:
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)

        # Caso Derecha-Derecha
        if balance < -1 and self._factor_balance(nodo.derecha) <= 0:
            return self._rotacion_izquierda(nodo)

        # Caso Derecha-Izquierda
        if balance < -1 and self._factor_balance(nodo.derecha) > 0:
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)

        return nodo

    def _rotacion_izquierda(self, z: NodoAVL) -> NodoAVL:
        y = z.derecha
        t2 = y.izquierda

        y.izquierda = z
        z.derecha = t2

        z.altura = 1 + max(self._altura(z.izquierda), self._altura(z.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))

        return y

    def _rotacion_derecha(self, z: NodoAVL) -> NodoAVL:
        y = z.izquierda
        t3 = y.derecha

        y.derecha = z
        z.izquierda = t3

        z.altura = 1 + max(self._altura(z.izquierda), self._altura(z.derecha))
        y.altura = 1 + max(self._altura(y.izquierda), self._altura(y.derecha))

        return y

    # =========================================================================
    # UTILIDADES
    # =========================================================================

    def _minimo(self, nodo: Optional[NodoAVL]) -> Optional[NodoAVL]:
        actual = nodo
        while actual and actual.izquierda:
            actual = actual.izquierda
        return actual

    def _maximo(self, nodo: Optional[NodoAVL]) -> Optional[NodoAVL]:
        actual = nodo
        while actual and actual.derecha:
            actual = actual.derecha
        return actual


