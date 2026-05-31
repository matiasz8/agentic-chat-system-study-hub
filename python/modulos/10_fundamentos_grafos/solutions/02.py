#!/usr/bin/env python3
"""
Solución 02 – BFS/DFS y detección de ciclos
Módulo 10: Fundamentos de Grafos
"""

from collections import deque, defaultdict


class GrafoConRecorrido:
    def __init__(self):
        self._adj: dict[str, list[str]] = defaultdict(list)

    def agregar_arista(self, u: str, v: str):
        self._adj[u].append(v)

    def bfs(self, inicio: str) -> list[str]:
        visitados, cola, orden = set(), deque([inicio]), []
        while cola:
            n = cola.popleft()
            if n in visitados:
                continue
            visitados.add(n)
            orden.append(n)
            cola.extend(v for v in self._adj.get(n, []) if v not in visitados)
        return orden

    def dfs(self, inicio: str, visitados: set | None = None) -> list[str]:
        if visitados is None:
            visitados = set()
        visitados.add(inicio)
        orden = [inicio]
        for v in self._adj.get(inicio, []):
            if v not in visitados:
                orden.extend(self.dfs(v, visitados))
        return orden

    def tiene_ciclo(self) -> bool:
        color: dict[str, str] = {}

        def dfs_c(n: str) -> bool:
            color[n] = "gris"
            for v in self._adj.get(n, []):
                if color.get(v) == "gris":
                    return True
                if color.get(v) != "negro" and dfs_c(v):
                    return True
            color[n] = "negro"
            return False

        todos = set(self._adj) | {v for vs in self._adj.values() for v in vs}
        return any(color.get(n) is None and dfs_c(n) for n in todos)


def main():
    g1 = GrafoConRecorrido()
    for u, v in [("inicio", "clasificar"), ("clasificar", "consultar"),
                 ("consultar", "responder"), ("responder", "fin")]:
        g1.agregar_arista(u, v)

    print("Grafo acíclico:")
    print(f"  BFS: {g1.bfs('inicio')}")
    print(f"  DFS: {g1.dfs('inicio')}")
    print(f"  Ciclo: {g1.tiene_ciclo()}")

    g2 = GrafoConRecorrido()
    for u, v in [("inicio", "clasificar"), ("clasificar", "ejecutar"),
                 ("ejecutar", "verificar"), ("verificar", "clasificar"),
                 ("verificar", "fin")]:
        g2.agregar_arista(u, v)

    print("\nGrafo con ciclo:")
    print(f"  BFS: {g2.bfs('inicio')}")
    print(f"  Ciclo: {g2.tiene_ciclo()}")


if __name__ == "__main__":
    main()
