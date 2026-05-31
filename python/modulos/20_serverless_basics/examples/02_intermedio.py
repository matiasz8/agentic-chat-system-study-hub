#!/usr/bin/env python3
"""
Ejemplo 02 – Intermedio: Cold start, caché y idempotencia
Módulo 20: Serverless Basics

Muestra:
  - Impacto del cold start con métricas de tiempo.
  - Caché en memoria (válida mientras la instancia vive).
  - Idempotencia: procesar el mismo evento dos veces da el mismo resultado.
"""

import time
import hashlib
import json
from functools import lru_cache


# ---------------------------------------------------------------------------
# Simulación de cold start vs warm start
# ---------------------------------------------------------------------------

class MetricasTiempo:
    def __init__(self):
        self._registros: list[dict] = []

    def registrar(self, nombre: str, duracion_ms: float, tipo: str):
        self._registros.append({"nombre": nombre, "duracion_ms": duracion_ms, "tipo": tipo})

    def mostrar_resumen(self):
        print("\n  Resumen de tiempos:")
        for r in self._registros:
            etiqueta = "🧊 cold" if r["tipo"] == "cold" else "🔥 warm"
            print(f"    {etiqueta} {r['nombre']:<20} {r['duracion_ms']:>7.1f} ms")


metricas = MetricasTiempo()


def inicializar_modelo_ia() -> dict:
    """Operación costosa de cold start: cargar un modelo."""
    inicio = time.perf_counter()
    time.sleep(0.15)  # simula descarga/carga del modelo
    duracion = (time.perf_counter() - inicio) * 1000
    metricas.registrar("carga_modelo", duracion, "cold")
    return {"modelo": "claude-3-5-sonnet", "cargado": True, "version": "1.0"}


# ---------------------------------------------------------------------------
# Caché en memoria (muere con la instancia Lambda)
# ---------------------------------------------------------------------------

_cache_stocks: dict[str, dict] = {}


def consultar_stock(medicamento_id: str) -> dict:
    """
    Consulta stock con caché en memoria.
    Primera llamada = "DB hit", siguientes = "cache hit".
    """
    if medicamento_id in _cache_stocks:
        print(f"  [CACHE HIT] {medicamento_id}")
        return _cache_stocks[medicamento_id]

    print(f"  [DB HIT] Consultando BD para {medicamento_id}…")
    time.sleep(0.03)  # latencia de BD simulada
    dato = {"medicamento_id": medicamento_id, "stock": 1500, "sede": "Central"}
    _cache_stocks[medicamento_id] = dato
    return dato


# ---------------------------------------------------------------------------
# Idempotencia: mismo evento → mismo resultado
# ---------------------------------------------------------------------------

_eventos_procesados: set[str] = set()


def _id_evento(evento: dict) -> str:
    """Genera un ID determinista para un evento (hash del contenido)."""
    contenido = json.dumps(evento, sort_keys=True)
    return hashlib.sha256(contenido.encode()).hexdigest()[:16]


def handler_idempotente(evento: dict) -> dict:
    """
    Handler que detecta y omite eventos duplicados.

    En producción se usaría DynamoDB como almacén de IDs:
        table.put_item(Item={'event_id': eid}, ConditionExpression='attribute_not_exists(event_id)')
    """
    eid = _id_evento(evento)

    if eid in _eventos_procesados:
        print(f"  [IDEMPOTENTE] Evento {eid!r} ya procesado. Devolviendo resultado anterior.")
        return {"statusCode": 200, "idempotente": True, "event_id": eid}

    _eventos_procesados.add(eid)
    print(f"  [PROCESANDO] Evento nuevo {eid!r}")
    time.sleep(0.02)

    resultado = {
        "statusCode": 200,
        "idempotente": False,
        "event_id": eid,
        "accion": evento.get("accion", "n/a"),
    }
    return resultado


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Módulo 20 – Ejemplo 02: Cold start, caché e idempotencia")
    print("=" * 60)

    # 1. Cold start del modelo
    print("\n1. Inicializando modelo (cold start)…")
    modelo = inicializar_modelo_ia()
    print(f"   Modelo cargado: {modelo}")

    # 2. Caché de stocks
    print("\n2. Consultas de stock con caché:")
    for mid in ["MED-001", "MED-002", "MED-001", "MED-002"]:
        resultado = consultar_stock(mid)
        print(f"   stock={resultado['stock']}")

    # 3. Idempotencia
    print("\n3. Procesando eventos (prueba de idempotencia):")
    evento_a = {"accion": "cancelar_orden", "orden_id": "ORD-999"}
    evento_b = {"accion": "cancelar_orden", "orden_id": "ORD-888"}

    for evento in [evento_a, evento_b, evento_a, evento_a]:
        r = handler_idempotente(evento)
        print(f"   idempotente={r['idempotente']} event_id={r['event_id']}")

    metricas.mostrar_resumen()
    print("\n✅ Cold start, caché e idempotencia demostrados.")


if __name__ == "__main__":
    main()
