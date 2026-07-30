#!/usr/bin/env python3
"""
Solución 01 – Grafo de flujo de agente
Módulo 10: Fundamentos de Grafos
"""

from collections import defaultdict


class GrafoDirigido:
    def __init__(self):
        self._adj: dict[str, list[str]] = defaultdict(list)
        self._nodos: set[str] = set()

    def agregar_nodo(self, nombre: str):
        self._nodos.add(nombre)

    def agregar_arista(self, origen: str, destino: str):
        self._nodos.update([origen, destino])
        self._adj[origen].append(destino)

    def vecinos(self, nodo: str) -> list[str]:
        return list(self._adj.get(nodo, []))

    def mostrar(self):
        for nodo in sorted(self._nodos):
            vs = self._adj.get(nodo, [])
            print(f"  {nodo} → {', '.join(vs) if vs else '(terminal)'}")


def main():
    g = GrafoDirigido()
    for nodo in ["inicio", "clasificar", "consultar", "responder", "fin"]:
        g.agregar_nodo(nodo)

    for u, v in [
        ("inicio", "clasificar"),
        ("clasificar", "consultar"),
        ("consultar", "responder"),
        ("responder", "fin"),
    ]:
        g.agregar_arista(u, v)

    print("Estructura del grafo:")
    g.mostrar()

    print(f"\nVecinos de 'clasificar': {g.vecinos('clasificar')}")
    print(f"Vecinos de 'fin'        : {g.vecinos('fin')}")


if __name__ == "__main__":
    main()
