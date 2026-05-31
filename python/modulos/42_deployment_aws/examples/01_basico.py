#!/usr/bin/env python3
"""Simulación básica del patrón AWS Lambda handler."""

from dataclasses import dataclass
import json


@dataclass
class FakeContext:
    aws_request_id: str
    function_name: str


def lambda_handler(event: dict, context: FakeContext) -> dict:
    try:
        action = event["action"]
        payload = event.get("payload", {})
        if action != "run-agent":
            raise ValueError(f"Acción no soportada: {action}")
        return {
            "statusCode": 200,
            "body": {
                "message": "Invocación procesada correctamente",
                "agent": payload.get("agent", "unknown"),
                "request_id": context.aws_request_id,
            },
        }
    except Exception as exc:
        return {
            "statusCode": 500,
            "body": {
                "error": str(exc),
                "request_id": context.aws_request_id,
            },
        }


def main() -> None:
    context = FakeContext("req-123", "ask-sage-lambda")
    print("=== Deployment AWS · Básico ===")
    print(json.dumps(lambda_handler({"action": "run-agent", "payload": {"agent": "triage"}}, context), indent=2, ensure_ascii=False))
    print(json.dumps(lambda_handler({"action": "delete-production"}, context), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
