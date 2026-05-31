#!/usr/bin/env python3
"""
Ejemplo 01 – Básico: Propagación de identidad entre servicios
Módulo 21: Identity Forwarding

Muestra cómo un token de usuario se propaga desde el frontend a través
del backend hasta los servicios downstream (BD, APIs internas).

En AWS AgentCore esto se implementa con Identity Forwarding nativo.
"""

import time
import uuid
import base64
import json


# ---------------------------------------------------------------------------
# Token de identidad (simulado)
# ---------------------------------------------------------------------------

def crear_token_usuario(usuario_id: str, rol: str, permisos: list[str]) -> str:
    """
    Crea un JWT simplificado (sin firma real) para demostración.
    En producción viene de Okta/Azure AD y se valida criptográficamente.
    """
    payload = {
        "sub": usuario_id,
        "rol": rol,
        "permisos": permisos,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()
    return f"eyJhbGciOiJIUzI1NiJ9.{payload_b64}.firma_simulada"


def decodificar_token(token: str) -> dict:
    """Decodifica el payload del token (sin verificar firma)."""
    partes = token.split(".")
    if len(partes) != 3:
        raise ValueError("Token inválido: se esperan 3 partes")
    padding = 4 - len(partes[1]) % 4
    payload_b64 = partes[1] + ("=" * padding)
    return json.loads(base64.b64decode(payload_b64).decode())


# ---------------------------------------------------------------------------
# Servicios simulados
# ---------------------------------------------------------------------------

def servicio_api_gateway(solicitud: dict) -> dict:
    """
    Punto de entrada (API Gateway).
    Extrae y valida el token, luego lo pasa al backend.
    """
    token = solicitud.get("headers", {}).get("Authorization", "").replace("Bearer ", "")
    if not token:
        return {"error": "Token ausente", "statusCode": 401}

    try:
        identidad = decodificar_token(token)
    except ValueError as e:
        return {"error": str(e), "statusCode": 401}

    print(f"  [API GW] Token validado para usuario {identidad['sub']!r} ({identidad['rol']})")

    # Pasar la identidad al backend (Identity Forwarding)
    return servicio_agente(
        solicitud=solicitud.get("body", {}),
        identidad=identidad,
        token_original=token,
    )


def servicio_agente(solicitud: dict, identidad: dict, token_original: str) -> dict:
    """
    Backend del agente. Usa la identidad para personalizar la respuesta
    y la pasa a la BD como contexto de auditoría.
    """
    print(f"  [AGENTE] Procesando solicitud de {identidad['sub']!r}")
    print(f"  [AGENTE] Permisos: {identidad['permisos']}")

    accion = solicitud.get("accion", "consultar")
    if accion not in identidad["permisos"]:
        return {"error": f"Sin permiso para: {accion!r}", "statusCode": 403}

    # Pasar token a la BD para trazabilidad
    resultado_bd = servicio_bd(
        accion=accion,
        datos=solicitud,
        usuario_id=identidad["sub"],
    )
    return {"statusCode": 200, "resultado": resultado_bd, "usuario": identidad["sub"]}


def servicio_bd(accion: str, datos: dict, usuario_id: str) -> dict:
    """
    Capa de datos. Recibe el usuario_id para auditoría y filtrado por rol.
    """
    print(f"  [BD] Ejecutando {accion!r} como usuario {usuario_id!r}")
    return {"accion_ejecutada": accion, "registros_afectados": 1, "auditado_por": usuario_id}


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Módulo 21 – Ejemplo 01: Propagación de identidad")
    print("=" * 60)

    # Usuario con permisos de lectura
    token_lector = crear_token_usuario(
        usuario_id="javier.garcia",
        rol="farmaceutico",
        permisos=["consultar", "ver_reportes"],
    )

    print("\n1. Usuario con permisos de lectura:")
    solicitud1 = {
        "headers": {"Authorization": f"Bearer {token_lector}"},
        "body": {"accion": "consultar", "medicamento_id": "MED-001"},
    }
    resultado1 = servicio_api_gateway(solicitud1)
    print(f"  → {resultado1}")

    # Usuario que intenta una acción sin permiso
    print("\n2. Usuario intentando acción sin permiso:")
    solicitud2 = {
        "headers": {"Authorization": f"Bearer {token_lector}"},
        "body": {"accion": "cancelar_orden", "orden_id": "ORD-999"},
    }
    resultado2 = servicio_api_gateway(solicitud2)
    print(f"  → {resultado2}")

    # Request sin token
    print("\n3. Request sin token (debe fallar con 401):")
    resultado3 = servicio_api_gateway({"headers": {}, "body": {}})
    print(f"  → {resultado3}")

    print("\n✅ Propagación de identidad demostrada.")


if __name__ == "__main__":
    main()
