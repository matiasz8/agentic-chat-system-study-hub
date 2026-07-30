#!/usr/bin/env python3
"""
Ejemplo 03 – Avanzado: Contexto de auditoría y principio de mínimo privilegio
Módulo 21: Identity Forwarding

Muestra:
  - Contexto de auditoría propagado automáticamente en cada operación.
  - Verificación del principio de mínimo privilegio (Cedar-like policy engine).
  - Registro inmutable de acciones (audit log).
"""

import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Contexto de auditoría
# ---------------------------------------------------------------------------


@dataclass
class ContextoAuditoria:
    """
    Contexto que viaja con cada operación.
    En AWS se implementa con X-Ray y CloudTrail.
    """

    trace_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    usuario_id: str = ""
    rol: str = ""
    ip_origen: str = ""
    accion_raiz: str = ""  # la acción del usuario que desencadenó todo

    def enriquecer(self, **kwargs) -> "ContextoAuditoria":
        """Crea una copia con campos adicionales (inmutabilidad)."""
        nuevo = ContextoAuditoria(
            trace_id=self.trace_id,
            usuario_id=self.usuario_id,
            rol=self.rol,
            ip_origen=self.ip_origen,
            accion_raiz=self.accion_raiz,
        )
        for k, v in kwargs.items():
            setattr(nuevo, k, v)
        return nuevo


# ---------------------------------------------------------------------------
# Registro de auditoría (inmutable)
# ---------------------------------------------------------------------------


class RegistroAuditoria:
    def __init__(self):
        self._entradas: list[dict] = []

    def registrar(self, ctx: ContextoAuditoria, operacion: str, resultado: str, datos: dict = None):
        entrada = {
            "timestamp": time.time(),
            "trace_id": ctx.trace_id,
            "usuario": ctx.usuario_id,
            "rol": ctx.rol,
            "ip": ctx.ip_origen,
            "accion_raiz": ctx.accion_raiz,
            "operacion": operacion,
            "resultado": resultado,
            "datos": datos or {},
        }
        self._entradas.append(entrada)
        icono = "✅" if resultado == "ok" else "❌"
        print(
            f"  [AUDIT {icono}] trace={ctx.trace_id} op={operacion!r} user={ctx.usuario_id!r} → {resultado}"
        )

    def exportar(self) -> list[dict]:
        return list(self._entradas)


auditoria = RegistroAuditoria()


# ---------------------------------------------------------------------------
# Motor de políticas (Cedar-like, simplificado)
# ---------------------------------------------------------------------------

# Políticas: (rol, accion, recurso) → permitido
POLITICAS: list[tuple[str, str, str]] = [
    ("farmaceutico", "leer", "stock"),
    ("farmaceutico", "leer", "reportes"),
    ("supervisor", "leer", "stock"),
    ("supervisor", "leer", "reportes"),
    ("supervisor", "escribir", "requisicion"),
    ("administrador", "*", "*"),
]


def esta_autorizado(rol: str, accion: str, recurso: str) -> bool:
    """
    Evalúa si (rol, accion, recurso) está permitido por las políticas.
    El administrador tiene acceso total ("*").
    """
    for p_rol, p_accion, p_recurso in POLITICAS:
        rol_ok = p_rol == rol or p_rol == "*"
        accion_ok = p_accion == accion or p_accion == "*"
        recurso_ok = p_recurso == recurso or p_recurso == "*"
        if rol_ok and accion_ok and recurso_ok:
            return True
    return False


# ---------------------------------------------------------------------------
# Decorador: inyectar verificación de autorización + auditoría
# ---------------------------------------------------------------------------


def autorizar(accion: str, recurso: str) -> Callable:
    """
    Decorador que aplica la política de autorización y registra la auditoría.

    Uso:
        @autorizar("escribir", "requisicion")
        def crear_requisicion(ctx, datos): ...
    """

    def decorador(func: Callable) -> Callable:
        def wrapper(ctx: ContextoAuditoria, *args, **kwargs):
            if not esta_autorizado(ctx.rol, accion, recurso):
                auditoria.registrar(ctx, f"{accion}:{recurso}", "denegado")
                raise PermissionError(
                    f"Rol {ctx.rol!r} no autorizado para {accion!r} en {recurso!r}"
                )
            resultado = func(ctx, *args, **kwargs)
            auditoria.registrar(ctx, f"{accion}:{recurso}", "ok", datos=kwargs)
            return resultado

        return wrapper

    return decorador


# ---------------------------------------------------------------------------
# Operaciones de negocio con autorización declarativa
# ---------------------------------------------------------------------------


@autorizar("leer", "stock")
def leer_stock(ctx: ContextoAuditoria, medicamento_id: str = "") -> dict:
    return {"medicamento_id": medicamento_id, "stock": 1500}


@autorizar("escribir", "requisicion")
def crear_requisicion(ctx: ContextoAuditoria, datos: dict = None) -> dict:
    return {"id": f"REQ-{str(uuid.uuid4())[:6]}", "datos": datos}


@autorizar("leer", "reportes")
def generar_reporte(ctx: ContextoAuditoria, tipo: str = "diario") -> dict:
    return {"reporte": tipo, "generado_por": ctx.usuario_id}


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 21 – Ejemplo 03: Auditoría y mínimo privilegio")
    print("=" * 60)

    # Supervisor realiza varias operaciones
    ctx_supervisor = ContextoAuditoria(
        usuario_id="mariana.lopez",
        rol="supervisor",
        ip_origen="10.0.1.42",
        accion_raiz="consulta_inventario",
    )

    print(f"\n1. Supervisor {ctx_supervisor.usuario_id!r} realizando operaciones:")
    stock = leer_stock(ctx_supervisor, medicamento_id="MED-001")
    print(f"   Stock: {stock}")

    req = crear_requisicion(ctx_supervisor, datos={"medicamento": "MED-001", "cantidad": 200})
    print(f"   Requisición: {req}")

    # Farmacéutico – solo lectura
    ctx_farm = ContextoAuditoria(
        usuario_id="javier.garcia",
        rol="farmaceutico",
        ip_origen="10.0.1.55",
        accion_raiz="ver_stock",
    )

    print(f"\n2. Farmacéutico {ctx_farm.usuario_id!r} intentando operaciones:")
    stock2 = leer_stock(ctx_farm, medicamento_id="MED-002")
    print(f"   Stock OK: {stock2}")

    try:
        crear_requisicion(ctx_farm, datos={"medicamento": "MED-002", "cantidad": 50})
    except PermissionError as e:
        print(f"   ❌ Denegado: {e}")

    # Resumen del audit log
    print(f"\n3. Audit log ({len(auditoria.exportar())} entradas):")
    for e in auditoria.exportar():
        ts = time.strftime("%H:%M:%S", time.localtime(e["timestamp"]))
        print(f"   {ts} | {e['usuario']:<18} | {e['operacion']:<22} | {e['resultado']}")

    print("\n✅ Contexto de auditoría y mínimo privilegio demostrados.")


if __name__ == "__main__":
    main()
