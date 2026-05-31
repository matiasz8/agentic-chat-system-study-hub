#!/usr/bin/env python3
"""
Solución 01 – Propagación de token entre servicios
Módulo 21: Identity Forwarding
"""

import base64
import json


def crear_token(usuario_id: str, permisos: list[str]) -> str:
    payload = json.dumps({"sub": usuario_id, "permisos": permisos})
    return base64.b64encode(payload.encode()).decode()


def decodificar_token(token: str) -> dict:
    try:
        return json.loads(base64.b64decode(token).decode())
    except Exception:
        raise ValueError("Token inválido")


def bd_consultar(usuario_id: str, medicamento_id: str) -> dict:
    print(f"  [BD] Consulta de {usuario_id!r}: medicamento {medicamento_id!r}")
    return {"medicamento_id": medicamento_id, "stock": 1500}


def agente(solicitud: dict, identidad: dict) -> dict:
    accion = solicitud.get("accion", "")
    if accion not in identidad["permisos"]:
        return {"statusCode": 403, "error": f"Sin permiso para {accion!r}"}
    resultado = bd_consultar(identidad["sub"], solicitud.get("medicamento_id", ""))
    return {"statusCode": 200, "resultado": resultado}


def api_gateway(solicitud: dict) -> dict:
    token = solicitud.get("headers", {}).get("Authorization", "")
    if not token:
        return {"statusCode": 401, "error": "Token ausente"}
    try:
        identidad = decodificar_token(token)
    except ValueError as e:
        return {"statusCode": 401, "error": str(e)}
    return agente(solicitud.get("body", {}), identidad)


def main():
    token = crear_token("javier.garcia", ["consultar"])

    print("Caso 1 – Acceso permitido:")
    print(api_gateway({"headers": {"Authorization": token}, "body": {"accion": "consultar", "medicamento_id": "MED-001"}}))

    print("\nCaso 2 – Acceso denegado:")
    print(api_gateway({"headers": {"Authorization": token}, "body": {"accion": "cancelar"}}))

    print("\nCaso 3 – Sin token:")
    print(api_gateway({"headers": {}, "body": {}}))


if __name__ == "__main__":
    main()
