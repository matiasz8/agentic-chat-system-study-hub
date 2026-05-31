#!/usr/bin/env python3
"""
Ejemplo 03 – Avanzado: Máquina de estados sobre grafo (State Machine)
Módulo 10: Fundamentos de Grafos

Muestra cómo un grafo dirigido puede actuar como una máquina de estados
que gestiona el flujo de un agente: cada nodo es un estado, cada arista
es una transición condicionada por el estado actual.

Esta es la intuición detrás de LangGraph: un StateGraph donde el
StateSchema define la memoria compartida y los nodos la modifican.
"""

from dataclasses import dataclass, field
from typing import Callable


# ---------------------------------------------------------------------------
# Estado compartido del agente (simula TypedDict / BaseModel de LangGraph)
# ---------------------------------------------------------------------------

@dataclass
class EstadoAgente:
    mensaje_usuario: str = ""
    intencion: str = ""           # "consulta" | "accion" | "desconocida"
    resultado_bd: dict = field(default_factory=dict)
    respuesta_final: str = ""
    intentos: int = 0
    max_intentos: int = 3


# ---------------------------------------------------------------------------
# Funciones de nodo (cada una recibe y modifica el estado)
# ---------------------------------------------------------------------------

def nodo_clasificar(estado: EstadoAgente) -> EstadoAgente:
    """Clasifica la intención del usuario."""
    msg = estado.mensaje_usuario.lower()
    if any(w in msg for w in ["stock", "inventario", "unidades", "cuántas"]):
        estado.intencion = "consulta"
    elif any(w in msg for w in ["cancela", "requisición", "pide", "solicita"]):
        estado.intencion = "accion"
    else:
        estado.intencion = "desconocida"
        estado.intentos += 1
    print(f"  [clasificar] intención detectada: {estado.intencion!r}")
    return estado


def nodo_consultar_bd(estado: EstadoAgente) -> EstadoAgente:
    """Simula la consulta al inventario."""
    estado.resultado_bd = {"medicamento": "X", "stock": 1500, "alerta": False}
    print(f"  [consultar_bd] resultado: {estado.resultado_bd}")
    return estado


def nodo_accion(estado: EstadoAgente) -> EstadoAgente:
    """Simula ejecutar una acción (ej. crear requisición)."""
    estado.resultado_bd = {"accion": "requisicion_creada", "id": "REQ-2024-001"}
    print(f"  [accion] ejecutada: {estado.resultado_bd}")
    return estado


def nodo_generar_respuesta(estado: EstadoAgente) -> EstadoAgente:
    """Genera la respuesta final para el usuario."""
    if "stock" in estado.resultado_bd:
        estado.respuesta_final = (
            f"El stock del medicamento {estado.resultado_bd['medicamento']} "
            f"es {estado.resultado_bd['stock']} unidades."
        )
    elif "accion" in estado.resultado_bd:
        estado.respuesta_final = (
            f"Acción completada: {estado.resultado_bd['accion']} "
            f"(ID: {estado.resultado_bd['id']})"
        )
    else:
        estado.respuesta_final = "No pude entender tu solicitud. ¿Puedes reformularla?"
    print(f"  [generar_respuesta] → {estado.respuesta_final!r}")
    return estado


# ---------------------------------------------------------------------------
# Máquina de estados (StateGraph minimalista)
# ---------------------------------------------------------------------------

class MaquinaEstados:
    def __init__(self, nodo_inicio: str, nodo_fin: str):
        self.nodo_inicio = nodo_inicio
        self.nodo_fin = nodo_fin
        self._nodos: dict[str, Callable] = {}
        self._aristas_fijas: dict[str, str] = {}
        self._aristas_cond: dict[str, Callable] = {}

    def agregar_nodo(self, nombre: str, funcion: Callable):
        self._nodos[nombre] = funcion

    def agregar_arista(self, origen: str, destino: str):
        self._aristas_fijas[origen] = destino

    def agregar_arista_condicional(self, origen: str, router: Callable):
        """
        En LangGraph:
            grafo.add_conditional_edges("clasificar", routing_fn, {...})
        """
        self._aristas_cond[origen] = router

    def ejecutar(self, estado: EstadoAgente) -> EstadoAgente:
        nodo_actual = self.nodo_inicio
        print(f"\n  Iniciando en nodo: {nodo_actual!r}")

        while nodo_actual != self.nodo_fin:
            fn = self._nodos.get(nodo_actual)
            if fn is None:
                raise RuntimeError(f"Nodo sin función: {nodo_actual!r}")

            estado = fn(estado)

            # Determinar siguiente nodo
            if nodo_actual in self._aristas_cond:
                nodo_siguiente = self._aristas_cond[nodo_actual](estado)
            elif nodo_actual in self._aristas_fijas:
                nodo_siguiente = self._aristas_fijas[nodo_actual]
            else:
                nodo_siguiente = self.nodo_fin

            print(f"  Transición: {nodo_actual!r} → {nodo_siguiente!r}")
            nodo_actual = nodo_siguiente

        fn = self._nodos.get(self.nodo_fin)
        if fn:
            estado = fn(estado)
        return estado


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Módulo 10 – Ejemplo 03: Máquina de estados (StateGraph)")
    print("=" * 60)

    # Construir la máquina de estados
    grafo = MaquinaEstados(nodo_inicio="clasificar", nodo_fin="generar_respuesta")
    grafo.agregar_nodo("clasificar",        nodo_clasificar)
    grafo.agregar_nodo("consultar_bd",      nodo_consultar_bd)
    grafo.agregar_nodo("accion",            nodo_accion)
    grafo.agregar_nodo("generar_respuesta", nodo_generar_respuesta)

    # Arista condicional después de clasificar
    def router_clasificar(estado: EstadoAgente) -> str:
        if estado.intencion == "consulta":
            return "consultar_bd"
        elif estado.intencion == "accion":
            return "accion"
        elif estado.intentos < estado.max_intentos:
            return "clasificar"  # reintentar
        return "generar_respuesta"

    grafo.agregar_arista_condicional("clasificar",   router_clasificar)
    grafo.agregar_arista("consultar_bd", "generar_respuesta")
    grafo.agregar_arista("accion",       "generar_respuesta")

    # Caso 1: consulta de stock
    print("\n--- Caso 1: Consulta de stock ---")
    estado1 = EstadoAgente(mensaje_usuario="¿Cuántas unidades hay del medicamento X?")
    resultado1 = grafo.ejecutar(estado1)
    print(f"\n  Respuesta al usuario: {resultado1.respuesta_final!r}")

    # Caso 2: acción
    print("\n--- Caso 2: Acción (requisición) ---")
    estado2 = EstadoAgente(mensaje_usuario="Solicita una requisición para medicamento Y")
    resultado2 = grafo.ejecutar(estado2)
    print(f"\n  Respuesta al usuario: {resultado2.respuesta_final!r}")

    print("\n✅ Máquina de estados sobre grafo demostrada.")


if __name__ == "__main__":
    main()
