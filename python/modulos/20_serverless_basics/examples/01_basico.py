#!/usr/bin/env python3
"""
Ejemplo 01 – Básico: Ciclo de vida de una función serverless
Módulo 20: Serverless Basics

Muestra el ciclo completo de una función Lambda:
  cold start → inicialización → ejecución → destrucción

El patrón "handler + inicialización fuera del handler" es la base
de cualquier función serverless bien escrita.
"""

import time
import uuid

# ---------------------------------------------------------------------------
# Inicialización fuera del handler (se ejecuta en cold start, una sola vez)
# ---------------------------------------------------------------------------

_INICIO_MODULO = time.perf_counter()
_CONEXION_BD_SIMULADA: dict | None = None


def _conectar_bd() -> dict:
    """Simula una conexión a BD costosa (ocurre solo en cold start)."""
    print("  [COLD START] Inicializando conexión a base de datos…")
    time.sleep(0.1)  # latencia de inicialización
    return {"host": "db.internal", "pool": 5, "conectada": True}


def obtener_conexion() -> dict:
    """Patrón 'lazy init': inicializa una sola vez, reutiliza en llamadas calientes."""
    global _CONEXION_BD_SIMULADA
    if _CONEXION_BD_SIMULADA is None:
        _CONEXION_BD_SIMULADA = _conectar_bd()
    return _CONEXION_BD_SIMULADA


# ---------------------------------------------------------------------------
# Handler (equivale a lambda_handler en AWS Lambda)
# ---------------------------------------------------------------------------


def handler(evento: dict, contexto: dict) -> dict:
    """
    Punto de entrada de la función serverless.

    En AWS Lambda:
        def lambda_handler(event, context):
            return { 'statusCode': 200, 'body': ... }
    """
    inicio = time.perf_counter()
    solicitud_id = contexto.get("aws_request_id", str(uuid.uuid4())[:8])

    print(f"  [HANDLER] request_id={solicitud_id!r} evento={evento}")

    # Reutilizar conexión (warm) o inicializarla (cold)
    bd = obtener_conexion()

    # Lógica de negocio
    accion = evento.get("accion", "consultar")
    if accion == "consultar":
        respuesta = {
            "medicamento": evento.get("medicamento_id", "unknown"),
            "stock": 1500,
            "bd_host": bd["host"],
        }
    else:
        respuesta = {"error": f"Acción desconocida: {accion!r}"}

    duracion_ms = (time.perf_counter() - inicio) * 1000
    return {
        "statusCode": 200,
        "solicitud_id": solicitud_id,
        "duracion_ms": round(duracion_ms, 2),
        "cuerpo": respuesta,
    }


# ---------------------------------------------------------------------------
# Flujo principal: simula invocaciones consecutivas
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 20 – Ejemplo 01: Ciclo de vida serverless")
    print("=" * 60)

    contexto_base = {"aws_request_id": "req-abc123", "region": "us-east-1"}

    # Invocación 1 – cold start (primera vez que se invoca la función)
    print("\n--- Invocación 1 (cold start) ---")
    r1 = handler({"accion": "consultar", "medicamento_id": "MED-001"}, contexto_base)
    print(f"  Resultado: {r1}")

    # Invocación 2 – warm start (la conexión ya existe)
    print("\n--- Invocación 2 (warm start) ---")
    contexto_base["aws_request_id"] = "req-def456"
    r2 = handler({"accion": "consultar", "medicamento_id": "MED-002"}, contexto_base)
    print(f"  Resultado: {r2}")
    print("  ✅ La conexión a BD NO se re-inicializó (warm start)")

    uptime = (time.perf_counter() - _INICIO_MODULO) * 1000
    print(f"\n  Tiempo total de vida de la instancia: {uptime:.1f} ms")
    print("\n✅ Ciclo de vida serverless demostrado.")


if __name__ == "__main__":
    main()
