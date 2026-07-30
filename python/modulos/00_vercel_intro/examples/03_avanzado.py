#!/usr/bin/env python3
"""
Ejemplo 03 – Avanzado: Streaming de tokens y multi-proveedor
Módulo 00: Introducción al Vercel AI SDK

Muestra:
  - streamText(): tokens llegan uno a uno (Server-Sent Events simulados)
  - Registro de múltiples proveedores (registry pattern)
  - Selección de proveedor en tiempo de ejecución
"""

import random
import time
from collections.abc import Iterator

# ---------------------------------------------------------------------------
# Simulación de streaming (Server-Sent Events)
# ---------------------------------------------------------------------------


def _tokenizar(texto: str) -> list[str]:
    """Divide un texto en tokens aproximados (palabras + puntuación)."""
    tokens = []
    for palabra in texto.split():
        tokens.append(palabra + " ")
    return tokens


def stream_texto(modelo: str, prompt: str) -> Iterator[str]:
    """
    Simula streamText() del SDK: genera tokens de forma incremental.

    En el SDK real (TypeScript):
        const { textStream } = await streamText({ model, prompt });
        for await (const chunk of textStream) { ... }
    """
    respuestas = {
        "gpt-4o": "El stock actual del medicamento solicitado es de 1.500 unidades. Hay bajo stock en dos sucursales del norte.",
        "claude-3-5-sonnet": "Según el inventario actualizado, dispone de 1.500 unidades disponibles. Alerta: sede norte y sede sur con stock crítico.",
        "gemini-1.5-pro": "Inventario consultado: 1.500 unidades totales. Recomendación: iniciar requisición para sedes norte y sur.",
    }
    texto = respuestas.get(modelo, f"[{modelo}] Respuesta no disponible.")
    tokens = _tokenizar(texto)

    for token in tokens:
        time.sleep(random.uniform(0.01, 0.03))  # latencia variable
        yield token


# ---------------------------------------------------------------------------
# Registro de proveedores (Provider Registry)
# ---------------------------------------------------------------------------


class RegistroProveedores:
    """
    Centraliza los proveedores disponibles.
    Equivale al createProviderRegistry() del Vercel AI SDK.
    """

    def __init__(self):
        self._proveedores: dict[str, dict] = {}

    def registrar(self, id_proveedor: str, modelos: list[str], region: str = "us-east-1"):
        self._proveedores[id_proveedor] = {"modelos": modelos, "region": region}
        print(f"  [REGISTRY] Registrado: {id_proveedor} ({', '.join(modelos)})")

    def resolver(self, id_proveedor: str, modelo: str) -> str:
        """Valida que el modelo exista en el proveedor dado."""
        if id_proveedor not in self._proveedores:
            raise KeyError(f"Proveedor desconocido: {id_proveedor!r}")
        info = self._proveedores[id_proveedor]
        if modelo not in info["modelos"]:
            raise ValueError(f"Modelo {modelo!r} no disponible en {id_proveedor!r}")
        return modelo

    def listar(self) -> dict:
        return dict(self._proveedores)


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 00 – Ejemplo 03: Streaming y multi-proveedor")
    print("=" * 60)

    # 1. Registrar proveedores
    print("\n1. Configurando registro de proveedores…")
    registro = RegistroProveedores()
    registro.registrar("openai", ["gpt-4o", "gpt-4o-mini"])
    registro.registrar("anthropic", ["claude-3-5-sonnet", "claude-3-haiku"])
    registro.registrar("google", ["gemini-1.5-pro", "gemini-1.5-flash"])

    # 2. Seleccionar proveedor en tiempo de ejecución
    proveedor_elegido = "anthropic"
    modelo_elegido = "claude-3-5-sonnet"
    registro.resolver(proveedor_elegido, modelo_elegido)
    print(f"\n2. Proveedor activo: {proveedor_elegido}/{modelo_elegido}")

    # 3. Streaming de tokens
    prompt = "¿Cuál es el stock del medicamento Z y hay alertas críticas?"
    print(f"\n3. Streaming tokens (prompt: «{prompt}»)")
    print("   Respuesta: ", end="", flush=True)

    tokens_recibidos = 0
    for token in stream_texto(modelo_elegido, prompt):
        print(token, end="", flush=True)
        tokens_recibidos += 1

    print(f"\n   [FIN STREAM] {tokens_recibidos} tokens recibidos")

    # 4. Comparar respuestas de distintos proveedores
    print("\n4. Comparando respuestas entre proveedores…")
    for pid, info in registro.listar().items():
        modelo = info["modelos"][0]
        tokens = list(stream_texto(modelo, "resumen rápido"))
        respuesta_corta = "".join(tokens[:5]) + "…"
        print(f"   {pid:<12} → {respuesta_corta}")

    print("\n✅ Streaming y registro de proveedores demostrados.")


if __name__ == "__main__":
    main()
