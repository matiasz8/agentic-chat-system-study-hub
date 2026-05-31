#!/usr/bin/env python3
"""
Solución 01 – Handler serverless con ciclo de vida
Módulo 20: Serverless Basics
"""

import time
import uuid

_CONEXION = None


def obtener_conexion() -> dict:
    global _CONEXION
    if _CONEXION is None:
        print("  [COLD START] Conectando a BD…")
        time.sleep(0.1)
        _CONEXION = {"host": "db.internal", "conectada": True}
    return _CONEXION


def handler(evento: dict, contexto: dict) -> dict:
    cold = _CONEXION is None
    inicio = time.perf_counter()
    bd = obtener_conexion()
    duracion = (time.perf_counter() - inicio) * 1000
    tipo = "cold start" if cold else "warm start"
    print(f"  [{tipo}] {duracion:.1f} ms | req={contexto.get('rid', '?')}")
    return {
        "statusCode": 200,
        "solicitud_id": contexto.get("rid", str(uuid.uuid4())[:8]),
        "cuerpo": {"medicamento": evento.get("id"), "stock": 1000, "bd": bd["host"]},
    }


def main():
    for i in range(3):
        r = handler({"id": f"MED-{i:03d}"}, {"rid": f"req-{i:03d}"})
        print(f"  → statusCode={r['statusCode']}")


if __name__ == "__main__":
    main()
