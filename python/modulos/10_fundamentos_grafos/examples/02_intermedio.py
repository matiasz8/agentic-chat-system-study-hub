#!/usr/bin/env python3
"""
Ejemplo 02 – Intermedio: Recorrido BFS/DFS y detección de ciclos
Módulo 10: Fundamentos de Grafos

Muestra dos algoritmos de recorrido (BFS y DFS) sobre el grafo del agente,
y cómo detectar ciclos (importante en LangGraph para evitar loops infinitos).
"""

from collections import deque, defaultdict


# ---------------------------------------------------------------------------
# Grafo con algoritmos de recorrido
# ---------------------------------------------------------------------------

class GrafoConRecorrido:
    def __init__(self):
        self._adj: dict[str, list[str]] = defaultdict(list)

    def agregar_arista(self, u: str, v: str):
        self._adj[u].append(v)

    # ------------------------------------------------------------------
    # BFS – Breadth-First Search (recorrido en amplitud)
    # En LangGraph: equivale a ejecutar todos los nodos del mismo nivel
    #               antes de avanzar al siguiente.
    # ------------------------------------------------------------------
    def bfs(self, inicio: str) -> list[str]:
        """Devuelve el orden de visita BFS desde 'inicio'."""
        visitados: set[str] = set()
        cola: deque[str] = deque([inicio])
        orden: list[str] = []

        while cola:
            nodo = cola.popleft()
            if nodo in visitados:
                continue
            visitados.add(nodo)
            orden.append(nodo)
            for vecino in self._adj.get(nodo, []):
                if vecino not in visitados:
                    cola.append(vecino)
        return orden

    # ------------------------------------------------------------------
    # DFS – Depth-First Search (recorrido en profundidad)
    # En LangGraph: el agente sigue un camino hasta el final antes de
    #               explorar rutas alternativas.
    # ------------------------------------------------------------------
    def dfs(self, inicio: str, visitados: set[str] | None = None) -> list[str]:
        """Devuelve el orden de visita DFS desde 'inicio' (recursivo)."""
        if visitados is None:
            visitados = set()
        visitados.add(inicio)
        orden = [inicio]
        for vecino in self._adj.get(inicio, []):
            if vecino not in visitados:
                orden.extend(self.dfs(vecino, visitados))
        return orden

    # ------------------------------------------------------------------
    # Detección de ciclos
    # ------------------------------------------------------------------
    def tiene_ciclo(self) -> bool:
        """
        Detecta si el grafo tiene algún ciclo (DFS con estado de color).
        BLANCO=no visitado, GRIS=en pila, NEGRO=completado.
        """
        color: dict[str, str] = {}

        def dfs_ciclo(nodo: str) -> bool:
            color[nodo] = "gris"
            for vecino in self._adj.get(nodo, []):
                if color.get(vecino) == "gris":
                    return True  # arista de retroceso → ciclo
                if color.get(vecino) != "negro" and dfs_ciclo(vecino):
                    return True
            color[nodo] = "negro"
            return False

        todos = set(self._adj.keys()) | {v for vs in self._adj.values() for v in vs}
        for nodo in todos:
            if color.get(nodo) is None:
                if dfs_ciclo(nodo):
                    return True
        return False


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Módulo 10 – Ejemplo 02: Recorrido BFS/DFS y ciclos")
    print("=" * 60)

    # Grafo acíclico (flujo normal de agente)
    print("\n1. Grafo acíclico – flujo normal del agente:")
    g_aciclico = GrafoConRecorrido()
    for u, v in [
        ("inicio", "clasificar"),
        ("clasificar", "consultar_bd"),
        ("clasificar", "accion_directa"),
        ("consultar_bd", "generar_resp"),
        ("accion_directa", "generar_resp"),
        ("generar_resp", "fin"),
    ]:
        g_aciclico.agregar_arista(u, v)

    print(f"  BFS desde 'inicio': {g_aciclico.bfs('inicio')}")
    print(f"  DFS desde 'inicio': {g_aciclico.dfs('inicio')}")
    print(f"  ¿Tiene ciclo?      : {g_aciclico.tiene_ciclo()}")

    # Grafo con ciclo (retroalimentación del agente)
    print("\n2. Grafo con ciclo – agente que puede reintentar:")
    g_ciclico = GrafoConRecorrido()
    for u, v in [
        ("inicio", "clasificar"),
        ("clasificar", "ejecutar"),
        ("ejecutar", "verificar"),
        ("verificar", "clasificar"),  # ← ciclo: vuelve a clasificar
        ("verificar", "fin"),
    ]:
        g_ciclico.agregar_arista(u, v)

    print(f"  BFS desde 'inicio': {g_ciclico.bfs('inicio')}")
    print(f"  ¿Tiene ciclo?      : {g_ciclico.tiene_ciclo()}")
    print("  ⚠️  Los ciclos en LangGraph requieren condición de salida.")

    print("\n✅ Recorrido BFS/DFS y detección de ciclos demostrados.")


if __name__ == "__main__":
    main()
