#!/usr/bin/env python3
"""
Solución 02 – Middleware de logging y límite de tokens
Módulo 00: Introducción al Vercel AI SDK
"""

import time
import functools
from typing import Callable


# ---------------------------------------------------------------------------
# Decoradores (middleware)
# ---------------------------------------------------------------------------

def registrar_llamada(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"→ Iniciando {func.__name__!r}")
        ts = time.perf_counter()
        try:
            resultado = func(*args, **kwargs)
            ms = (time.perf_counter() - ts) * 1000
            print(f"← OK en {ms:.1f} ms")
            return resultado
        except Exception as exc:
            ms = (time.perf_counter() - ts) * 1000
            print(f"← ERROR en {ms:.1f} ms: {exc}")
            raise
    return wrapper


def limitar_tokens(max_tokens: int) -> Callable:
    def decorador(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(proveedor, mensaje: str, *args, **kwargs):
            tokens = len(mensaje.split())
            if tokens > max_tokens:
                raise ValueError(
                    f"Mensaje demasiado largo: {tokens} tokens > máximo {max_tokens}"
                )
            return func(proveedor, mensaje, *args, **kwargs)
        return wrapper
    return decorador


# ---------------------------------------------------------------------------
# Función principal con decoradores aplicados
# ---------------------------------------------------------------------------

class Proveedor:
    def __init__(self, nombre: str, modelo: str):
        self.nombre = nombre
        self.modelo = modelo


@registrar_llamada
@limitar_tokens(max_tokens=20)
def llamar_proveedor(proveedor: Proveedor, mensaje: str) -> dict:
    time.sleep(0.04)
    return {
        "texto": f"[{proveedor.modelo}] Respuesta a: '{mensaje}'",
        "tokens_entrada": len(mensaje.split()),
        "tokens_salida": 8,
    }


def main():
    p = Proveedor("anthropic", "claude-3-5-sonnet")

    # Caso 1: llamada exitosa
    print("--- Caso exitoso ---")
    resultado = llamar_proveedor(p, "¿Cuántas unidades del medicamento Y?")
    print("Texto:", resultado["texto"])

    # Caso 2: mensaje demasiado largo
    print("\n--- Caso con error (mensaje largo) ---")
    mensaje_largo = " ".join(["palabra"] * 25)
    try:
        llamar_proveedor(p, mensaje_largo)
    except ValueError:
        pass  # El decorador ya imprimió el error


if __name__ == "__main__":
    main()
