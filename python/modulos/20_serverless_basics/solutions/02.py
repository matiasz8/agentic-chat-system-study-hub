#!/usr/bin/env python3
"""
Solución 02 – Idempotencia con registro de eventos
Módulo 20: Serverless Basics
"""

import hashlib
import json
import time

_eventos_procesados: set[str] = set()


def generar_id_evento(evento: dict) -> str:
    contenido = json.dumps(evento, sort_keys=True)
    return hashlib.sha256(contenido.encode()).hexdigest()[:16]


def handler_idempotente(evento: dict) -> dict:
    eid = generar_id_evento(evento)
    if eid in _eventos_procesados:
        print(f"  [DUP] evento {eid!r} ya procesado")
        return {"statusCode": 200, "idempotente": True, "event_id": eid}

    _eventos_procesados.add(eid)
    time.sleep(0.01)
    print(f"  [OK] procesando evento {eid!r} → {evento.get('accion')}")
    return {"statusCode": 200, "idempotente": False, "event_id": eid}


def main():
    eventos = [
        {"accion": "cancelar", "orden": "ORD-001"},
        {"accion": "cancelar", "orden": "ORD-002"},
        {"accion": "cancelar", "orden": "ORD-001"},  # duplicado
        {"accion": "cancelar", "orden": "ORD-001"},  # duplicado
    ]
    for e in eventos:
        r = handler_idempotente(e)
        print(f"    idempotente={r['idempotente']}")


if __name__ == "__main__":
    main()
