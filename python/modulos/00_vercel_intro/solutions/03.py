#!/usr/bin/env python3
"""
Solución 03 – Registro de proveedores y streaming
Módulo 00: Introducción al Vercel AI SDK
"""

import random
import time
from collections.abc import Iterator


class RegistroProveedores:
    def __init__(self):
        self._reg: dict[str, list[str]] = {}

    def registrar(self, id_proveedor: str, modelos: list[str]):
        self._reg[id_proveedor] = modelos
        print(f"  [REGISTRY] {id_proveedor}: {modelos}")

    def resolver(self, id_proveedor: str, modelo: str) -> str:
        if id_proveedor not in self._reg:
            raise KeyError(f"Proveedor desconocido: {id_proveedor!r}")
        if modelo not in self._reg[id_proveedor]:
            raise ValueError(f"Modelo {modelo!r} no disponible en {id_proveedor!r}")
        return modelo


def stream_tokens(modelo: str, texto: str) -> Iterator[str]:
    for palabra in texto.split():
        time.sleep(random.uniform(0.01, 0.03))
        yield palabra + " "


def main():
    registro = RegistroProveedores()
    registro.registrar("openai", ["gpt-4o", "gpt-4o-mini"])
    registro.registrar("anthropic", ["claude-3-5-sonnet"])

    # Proveedor válido
    try:
        registro.resolver("openai", "gpt-4o")
        print("\nStreaming con gpt-4o:")
        print("  ", end="", flush=True)
        for token in stream_tokens(
            "gpt-4o", "El stock es de 1500 unidades disponibles en sede central."
        ):
            print(token, end="", flush=True)
        print()
    except (KeyError, ValueError) as e:
        print(f"Error: {e}")

    # Proveedor inválido
    print("\nIntentando proveedor inválido:")
    try:
        registro.resolver("google", "gemini-1.5-pro")
    except KeyError as e:
        print(f"  Error esperado: {e}")


if __name__ == "__main__":
    main()
