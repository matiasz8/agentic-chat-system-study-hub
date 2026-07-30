#!/usr/bin/env python3
"""
Solución 02 – Tokens de alcance reducido
Módulo 21: Identity Forwarding
"""

import time
import uuid
from dataclasses import dataclass, field

POLITICAS = {
    "farmaceutico": ["leer:stock", "leer:reportes"],
    "supervisor": ["leer:stock", "leer:reportes", "escribir:requisicion"],
}


@dataclass
class TokenAlcance:
    usuario_id: str
    operacion: str
    recurso: str
    expira_en: float
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def esta_vigente(self) -> bool:
        return time.time() < self.expira_en


def generar_token(
    usuario_id: str, rol: str, operacion: str, recurso: str, duracion_seg: int = 300
) -> TokenAlcance:
    if operacion not in POLITICAS.get(rol, []):
        raise PermissionError(f"Rol {rol!r} no puede realizar {operacion!r}")
    return TokenAlcance(
        usuario_id=usuario_id,
        operacion=operacion,
        recurso=recurso,
        expira_en=time.time() + duracion_seg,
    )


def validar_token(token: TokenAlcance, operacion_requerida: str) -> bool:
    return token.esta_vigente() and token.operacion == operacion_requerida


def main():
    # Token válido
    t = generar_token("javier", "farmaceutico", "leer:stock", "inventario/MED-001")
    print(f"Token generado: {t.id}, vigente={t.esta_vigente()}")
    print(f"Válido para leer:stock: {validar_token(t, 'leer:stock')}")

    # Operación no permitida
    try:
        generar_token("javier", "farmaceutico", "escribir:requisicion", "requisiciones/*")
    except PermissionError as e:
        print(f"Denegado: {e}")

    # Token expirado
    t_exp = TokenAlcance("u", "leer:stock", "r", expira_en=time.time() - 1)
    print(f"Token expirado válido: {validar_token(t_exp, 'leer:stock')}")


if __name__ == "__main__":
    main()
