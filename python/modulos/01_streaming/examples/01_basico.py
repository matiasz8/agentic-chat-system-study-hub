#!/usr/bin/env python3
"""Ejemplo básico de streaming de tokens con un generador."""

from __future__ import annotations

import sys
import time
from collections.abc import Iterator

DELAY_SECONDS = 0.12


def fake_llm_stream(text: str, delay: float = DELAY_SECONDS) -> Iterator[str]:
    for token in text.split():
        time.sleep(delay)
        yield token


def main() -> None:
    respuesta = (
        "Streaming permite que la interfaz muestre progreso antes de tener la respuesta completa."
    )
    print("=== Demo básica: token streaming ===")
    print("Modelo: generando respuesta...\n")

    reconstruccion: list[str] = []
    for token in fake_llm_stream(respuesta):
        reconstruccion.append(token)
        sys.stdout.write(f"[token] {token}\n")
        sys.stdout.flush()

    print("\nRespuesta final reconstruida:")
    print(" ".join(reconstruccion))
    print("\nObserva que cada token apareció antes del resultado final.")


if __name__ == "__main__":
    main()
