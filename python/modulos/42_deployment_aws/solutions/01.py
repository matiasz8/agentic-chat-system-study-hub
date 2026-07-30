#!/usr/bin/env python3
"""Solución del ejercicio 1 del módulo Deployment AWS."""

import json


def process_message(payload: dict) -> str:
    action = payload.get("action")
    if action != "index-document":
        raise ValueError(f"Acción inválida: {action}")
    return f"Documento {payload.get('document_id', 'unknown')} indexado"


def lambda_handler(event: dict) -> dict:
    dead_letter_queue: list[dict] = []
    processed = 0
    failures = 0
    for record in event.get("Records", []):
        try:
            payload = json.loads(record["body"])
            print(process_message(payload))
            processed += 1
        except Exception as exc:
            failures += 1
            dead_letter_queue.append({"record": record, "error": str(exc)})
    return {"processed": processed, "failures": failures, "dead_letter_queue": dead_letter_queue}


def main() -> None:
    event = {
        "Records": [
            {"body": json.dumps({"action": "index-document", "document_id": "a1"})},
            {"body": json.dumps({"action": "delete-prod", "document_id": "a2"})},
        ]
    }
    print("=== Solución 1 ===")
    print(json.dumps(lambda_handler(event), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
