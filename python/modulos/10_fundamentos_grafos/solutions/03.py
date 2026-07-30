#!/usr/bin/env python3
"""
Solución 03 – Máquina de estados con aristas condicionales
Módulo 10: Fundamentos de Grafos
"""

from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Estado:
    mensaje: str = ""
    intencion: str = ""
    resultado: str = ""
    respuesta: str = ""


class MaquinaEstados:
    def __init__(self, inicio: str, fin: str):
        self.inicio = inicio
        self.fin = fin
        self._nodos: dict[str, Callable] = {}
        self._fijas: dict[str, str] = {}
        self._cond: dict[str, Callable] = {}

    def agregar_nodo(self, nombre: str, fn: Callable):
        self._nodos[nombre] = fn

    def agregar_arista(self, u: str, v: str):
        self._fijas[u] = v

    def agregar_arista_condicional(self, u: str, router: Callable):
        self._cond[u] = router

    def ejecutar(self, estado: Estado) -> Estado:
        actual = self.inicio
        while actual != self.fin:
            estado = self._nodos[actual](estado)
            if actual in self._cond:
                siguiente = self._cond[actual](estado)
            else:
                siguiente = self._fijas.get(actual, self.fin)
            print(f"  {actual} → {siguiente}")
            actual = siguiente
        if self.fin in self._nodos:
            estado = self._nodos[self.fin](estado)
        return estado


def clasificar(e: Estado) -> Estado:
    e.intencion = "consulta" if "stock" in e.mensaje.lower() else "accion"
    return e


def consultar(e: Estado) -> Estado:
    e.resultado = "stock=1500"
    return e


def ejecutar_accion(e: Estado) -> Estado:
    e.resultado = "requisicion_creada"
    return e


def responder(e: Estado) -> Estado:
    e.respuesta = f"Resultado: {e.resultado}"
    return e


def main():
    maq = MaquinaEstados("clasificar", "responder")
    maq.agregar_nodo("clasificar", clasificar)
    maq.agregar_nodo("consultar", consultar)
    maq.agregar_nodo("ejecutar", ejecutar_accion)
    maq.agregar_nodo("responder", responder)
    maq.agregar_arista_condicional(
        "clasificar", lambda e: "consultar" if e.intencion == "consulta" else "ejecutar"
    )
    maq.agregar_arista("consultar", "responder")
    maq.agregar_arista("ejecutar", "responder")

    print("--- Ruta consulta ---")
    r1 = maq.ejecutar(Estado(mensaje="¿Cuánto stock hay?"))
    print(f"  Respuesta: {r1.respuesta}")

    print("\n--- Ruta acción ---")
    r2 = maq.ejecutar(Estado(mensaje="Crear una requisición"))
    print(f"  Respuesta: {r2.respuesta}")


if __name__ == "__main__":
    main()
