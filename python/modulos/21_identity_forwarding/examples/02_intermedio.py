#!/usr/bin/env python3
"""
Ejemplo 02 – Intermedio: Tokens de alcance reducido (scoped tokens)
Módulo 21: Identity Forwarding

Muestra el patrón de "token downscoping": cuando el agente necesita llamar
a un servicio externo, genera un token con permisos mínimos para esa
operación específica (principio de mínimo privilegio).

En AWS AgentCore esto se implementa con IAM Roles y Cedar policies.
"""

import time
import uuid
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Gestión de tokens
# ---------------------------------------------------------------------------


@dataclass
class ContextoIdentidad:
    """Identidad del usuario durante toda la sesión del agente."""

    usuario_id: str
    rol: str
    permisos_globales: list[str]
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    creado_en: float = field(default_factory=time.time)


@dataclass
class TokenAlcanceReducido:
    """
    Token efímero con permisos mínimos para una operación concreta.
    Equivale a un 'scoped credential' en AWS STS:
        sts.assume_role(RoleArn=..., Policy=limited_policy, DurationSeconds=900)
    """

    usuario_id: str
    operacion: str  # p.ej. "leer:stock"
    recurso: str  # p.ej. "inventario/MED-001"
    expira_en: float  # timestamp Unix
    token_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def esta_vigente(self) -> bool:
        return time.time() < self.expira_en

    def __str__(self) -> str:
        return (
            f"ScopedToken(id={self.token_id}, op={self.operacion!r}, "
            f"recurso={self.recurso!r}, vigente={self.esta_vigente()})"
        )


# ---------------------------------------------------------------------------
# Servicio de autorización (simplificado)
# ---------------------------------------------------------------------------

# Tabla de operaciones permitidas por rol
POLITICA_ROLES = {
    "farmaceutico": ["leer:stock", "leer:reportes"],
    "supervisor": ["leer:stock", "leer:reportes", "escribir:requisicion"],
    "administrador": ["leer:stock", "leer:reportes", "escribir:requisicion", "cancelar:orden"],
}


def generar_token_alcance(
    contexto: ContextoIdentidad,
    operacion: str,
    recurso: str,
    duracion_seg: int = 300,
) -> TokenAlcanceReducido:
    """
    Genera un token de alcance reducido si el usuario tiene permiso.
    Lanza PermissionError si no.
    """
    permisos_rol = POLITICA_ROLES.get(contexto.rol, [])
    if operacion not in permisos_rol:
        raise PermissionError(
            f"Usuario {contexto.usuario_id!r} (rol={contexto.rol!r}) "
            f"no tiene permiso para {operacion!r}"
        )

    token = TokenAlcanceReducido(
        usuario_id=contexto.usuario_id,
        operacion=operacion,
        recurso=recurso,
        expira_en=time.time() + duracion_seg,
    )
    print(f"  [TOKEN] Generado token de alcance para {operacion!r}: {token.token_id!r}")
    return token


# ---------------------------------------------------------------------------
# Servicio downstream que valida el token de alcance
# ---------------------------------------------------------------------------


def llamar_servicio_inventario(token: TokenAlcanceReducido, medicamento_id: str) -> dict:
    """Solo acepta tokens con la operación correcta y vigentes."""
    if not token.esta_vigente():
        raise RuntimeError(f"Token {token.token_id!r} expirado")
    if token.operacion != "leer:stock":
        raise PermissionError(
            f"Operación incorrecta: se requiere 'leer:stock', recibido {token.operacion!r}"
        )

    print(f"  [INVENTARIO] Consulta autorizada por token {token.token_id!r}")
    return {"medicamento_id": medicamento_id, "stock": 1500, "autorizado_por": token.usuario_id}


def llamar_servicio_requisicion(token: TokenAlcanceReducido, datos: dict) -> dict:
    if not token.esta_vigente():
        raise RuntimeError(f"Token {token.token_id!r} expirado")
    if token.operacion != "escribir:requisicion":
        raise PermissionError(f"Se requiere 'escribir:requisicion', recibido {token.operacion!r}")

    print(f"  [REQUISICION] Creada con token {token.token_id!r}")
    return {"requisicion_id": f"REQ-{str(uuid.uuid4())[:6]}", "datos": datos}


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 21 – Ejemplo 02: Tokens de alcance reducido")
    print("=" * 60)

    # Supervisor: puede leer y escribir
    supervisor = ContextoIdentidad(
        usuario_id="mariana.lopez",
        rol="supervisor",
        permisos_globales=["leer:stock", "leer:reportes", "escribir:requisicion"],
    )

    print(f"\n1. Usuario: {supervisor.usuario_id!r} (rol={supervisor.rol!r})")

    # Generar token para consulta de stock
    print("\n2. Solicitando token para 'leer:stock'…")
    t_leer = generar_token_alcance(supervisor, "leer:stock", "inventario/MED-001")
    resultado = llamar_servicio_inventario(t_leer, "MED-001")
    print(f"   Resultado: {resultado}")

    # Generar token para crear requisición
    print("\n3. Solicitando token para 'escribir:requisicion'…")
    t_escribir = generar_token_alcance(supervisor, "escribir:requisicion", "requisiciones/*")
    resultado2 = llamar_servicio_requisicion(
        t_escribir, {"medicamento": "MED-001", "cantidad": 200}
    )
    print(f"   Resultado: {resultado2}")

    # Farmacéutico intentando crear requisición (sin permiso)
    print("\n4. Farmacéutico intentando crear requisición (debe fallar)…")
    farmaceutico = ContextoIdentidad("javier.garcia", "farmaceutico", ["leer:stock"])
    try:
        generar_token_alcance(farmaceutico, "escribir:requisicion", "requisiciones/*")
    except PermissionError as e:
        print(f"   ❌ Denegado: {e}")

    print("\n✅ Tokens de alcance reducido demostrados.")


if __name__ == "__main__":
    main()
