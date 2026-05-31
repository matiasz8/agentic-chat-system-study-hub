#!/usr/bin/env python3
"""
Solución 03 – Registro de auditoría y motor de políticas
Módulo 21: Identity Forwarding
"""

import time
import functools
from dataclasses import dataclass
from typing import Callable

POLITICAS = [
    ("farmaceutico", "leer",     "stock"),
    ("farmaceutico", "leer",     "reportes"),
    ("supervisor",   "leer",     "stock"),
    ("supervisor",   "escribir", "requisicion"),
    ("administrador", "*",       "*"),
]


def esta_autorizado(rol: str, accion: str, recurso: str) -> bool:
    for p_rol, p_acc, p_rec in POLITICAS:
        if (p_rol == rol or p_rol == "*") and (p_acc == accion or p_acc == "*") and (p_rec == recurso or p_rec == "*"):
            return True
    return False


class RegistroAuditoria:
    def __init__(self):
        self._log: list[dict] = []

    def registrar(self, usuario: str, operacion: str, resultado: str):
        self._log.append({"ts": time.strftime("%H:%M:%S"), "usuario": usuario, "op": operacion, "resultado": resultado})
        icono = "✅" if resultado == "ok" else "❌"
        print(f"  [AUDIT {icono}] {usuario} | {operacion} | {resultado}")

    def mostrar(self):
        print("\nAudit log completo:")
        for e in self._log:
            print(f"  {e['ts']} | {e['usuario']:<18} | {e['op']:<22} | {e['resultado']}")


auditoria = RegistroAuditoria()


@dataclass
class Ctx:
    usuario_id: str
    rol: str


def autorizar(accion: str, recurso: str) -> Callable:
    def decorador(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(ctx: Ctx, *args, **kwargs):
            if not esta_autorizado(ctx.rol, accion, recurso):
                auditoria.registrar(ctx.usuario_id, f"{accion}:{recurso}", "denegado")
                raise PermissionError(f"{ctx.rol!r} no puede {accion!r}:{recurso!r}")
            resultado = func(ctx, *args, **kwargs)
            auditoria.registrar(ctx.usuario_id, f"{accion}:{recurso}", "ok")
            return resultado
        return wrapper
    return decorador


@autorizar("leer", "stock")
def leer_stock(ctx: Ctx) -> dict:
    return {"stock": 1500}


@autorizar("escribir", "requisicion")
def crear_requisicion(ctx: Ctx) -> dict:
    return {"id": "REQ-001"}


def main():
    farm = Ctx("javier", "farmaceutico")
    sup  = Ctx("mariana", "supervisor")

    leer_stock(farm)
    leer_stock(sup)
    crear_requisicion(sup)

    try:
        crear_requisicion(farm)
    except PermissionError:
        pass

    auditoria.mostrar()


if __name__ == "__main__":
    main()
