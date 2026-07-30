#!/usr/bin/env python3
"""
Ejemplo 01 – Básico: Grafo dirigido con nodos y aristas
Módulo 10: Fundamentos de Grafos

Muestra cómo representar un grafo dirigido usando un diccionario de
adyacencia, agregar nodos y aristas, e inspeccionar la estructura.

Relación con LangGraph: un "StateGraph" es exactamente este grafo donde
los nodos son funciones y las aristas son transiciones.
"""

from collections import defaultdict

# ---------------------------------------------------------------------------
# Representación de un grafo dirigido simple
# ---------------------------------------------------------------------------


class GrafoDirigido:
    """
    Grafo dirigido con lista de adyacencia.

    En LangGraph:
        grafo = StateGraph(MiState)
        grafo.add_node("clasificar", clasificar_fn)
        grafo.add_node("responder", responder_fn)
        grafo.add_edge("clasificar", "responder")
    """

    def __init__(self):
        self._adyacencia: dict[str, list[str]] = defaultdict(list)
        self._nodos: set[str] = set()

    def agregar_nodo(self, nombre: str, descripcion: str = ""):
        """Registra un nodo (equivale a add_node en LangGraph)."""
        self._nodos.add(nombre)
        if nombre not in self._adyacencia:
            self._adyacencia[nombre] = []
        if descripcion:
            print(f"  [NODO] '{nombre}': {descripcion}")

    def agregar_arista(self, origen: str, destino: str):
        """Conecta dos nodos (equivale a add_edge en LangGraph)."""
        self._nodos.add(origen)
        self._nodos.add(destino)
        self._adyacencia[origen].append(destino)
        print(f"  [ARISTA] '{origen}' → '{destino}'")

    def vecinos(self, nodo: str) -> list[str]:
        """Devuelve los nodos alcanzables desde 'nodo'."""
        return list(self._adyacencia.get(nodo, []))

    def mostrar(self):
        print("\n  Estructura del grafo:")
        for nodo in sorted(self._nodos):
            siguientes = self._adyacencia.get(nodo, [])
            if siguientes:
                print(f"    {nodo} → {', '.join(siguientes)}")
            else:
                print(f"    {nodo} (terminal)")


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 10 – Ejemplo 01: Grafo dirigido básico")
    print("=" * 60)

    # Crear el grafo (equivalente a un StateGraph de LangGraph)
    print("\n1. Definiendo nodos del grafo de agente farmacéutico:")
    g = GrafoDirigido()
    g.agregar_nodo("inicio", "punto de entrada del flujo")
    g.agregar_nodo("clasificar", "clasifica la intención del usuario")
    g.agregar_nodo("consultar_bd", "consulta el inventario en BD")
    g.agregar_nodo("generar_resp", "genera la respuesta final")
    g.agregar_nodo("fin", "nodo terminal")

    print("\n2. Conectando nodos con aristas:")
    g.agregar_arista("inicio", "clasificar")
    g.agregar_arista("clasificar", "consultar_bd")
    g.agregar_arista("consultar_bd", "generar_resp")
    g.agregar_arista("generar_resp", "fin")

    # Mostrar estructura
    g.mostrar()

    # Inspeccionar vecinos
    print("\n3. ¿Qué sigue después de 'clasificar'?")
    print(f"   Vecinos: {g.vecinos('clasificar')}")

    print("\n4. ¿Qué sigue después de 'fin'?")
    print(f"   Vecinos: {g.vecinos('fin')} (nodo terminal, flujo termina aquí)")

    print("\n✅ Grafo básico con nodos y aristas creado correctamente.")


if __name__ == "__main__":
    main()
