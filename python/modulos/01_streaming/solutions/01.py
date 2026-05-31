#!/usr/bin/env python3
"""Solución al ejercicio básico de streaming incremental."""

from __future__ import annotations

import sys
import time
from typing import Iterator


def stream_fake_response(texto: str, delay: float = 0.1) -> Iterator[str]:
    for token in texto.split():
        time.sleep(delay)
        yield token


def main() -> None:
    texto = "Una buena UX muestra avance desde el primer token disponible."
    reconstruida: list[str] = []

    print("=== Solución 1 ===")
    for indice, token in enumerate(stream_fake_response(texto), start=1):
        reconstruida.append(token)
        sys.stdout.write(f"Token {indice}: {token}\n")
        sys.stdout.flush()

    print("\nRespuesta completa:")
    print(" ".join(reconstruida))


if __name__ == "__main__":
    main()
