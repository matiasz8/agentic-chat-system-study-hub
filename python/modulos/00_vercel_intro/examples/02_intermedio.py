#!/usr/bin/env python3
"""
Ejemplo 02 – Intermedio: Configuración de proveedor y middleware
Módulo 00: Introducción al Vercel AI SDK

Muestra cómo configurar parámetros del proveedor (temperatura, tokens máximos)
y cómo añadir middleware de logging/métricas antes y después de cada llamada.
"""

import time
import functools
from dataclasses import dataclass, field
from typing import Callable


# ---------------------------------------------------------------------------
# Modelos de datos
# ---------------------------------------------------------------------------

@dataclass
class ConfigProveedor:
    nombre: str
    modelo: str
    temperatura: float = 0.7
    max_tokens: int = 1024
    timeout_seg: float = 30.0


@dataclass
class Respuesta:
    texto: str
    tokens_entrada: int
    tokens_salida: int
    duracion_ms: float
    modelo: str


# ---------------------------------------------------------------------------
# Middleware (decorador de función)
# ---------------------------------------------------------------------------

def middleware_logging(func: Callable) -> Callable:
    """
    Middleware que registra cada llamada al SDK.
    Equivale al middleware customizable del Vercel AI SDK:
        wrapLanguageModel({ model, middleware: [...] })
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ts_inicio = time.perf_counter()
        print(f"  [LOG] → Llamando a {func.__name__!r}")
        try:
            resultado = func(*args, **kwargs)
            duracion = (time.perf_counter() - ts_inicio) * 1000
            print(f"  [LOG] ← OK en {duracion:.1f} ms")
            return resultado
        except Exception as exc:
            duracion = (time.perf_counter() - ts_inicio) * 1000
            print(f"  [LOG] ← ERROR en {duracion:.1f} ms: {exc}")
            raise
    return wrapper


# ---------------------------------------------------------------------------
# Cliente del SDK
# ---------------------------------------------------------------------------

class ClienteSDK:
    def __init__(self, config: ConfigProveedor):
        self.config = config

    @middleware_logging
    def generar_texto(self, mensajes: list[dict]) -> Respuesta:
        """Simula generateText() con parámetros del proveedor."""
        time.sleep(0.04)  # latencia simulada

        contenido_usuario = next(
            (m["content"] for m in reversed(mensajes) if m["rol"] == "usuario"), ""
        )
        tokens_in = len(contenido_usuario.split())
        tokens_out = min(self.config.max_tokens, 20)
        texto = (
            f"[{self.config.modelo} T={self.config.temperatura}] "
            f"Respondo a: «{contenido_usuario}»"
        )
        return Respuesta(
            texto=texto,
            tokens_entrada=tokens_in,
            tokens_salida=tokens_out,
            duracion_ms=40.0,
            modelo=self.config.modelo,
        )


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Módulo 00 – Ejemplo 02: Configuración y middleware")
    print("=" * 60)

    # 1. Configurar proveedor con parámetros específicos
    config = ConfigProveedor(
        nombre="anthropic",
        modelo="claude-3-5-sonnet",
        temperatura=0.3,   # más determinista para farmacéutica
        max_tokens=512,
        timeout_seg=15.0,
    )
    print(f"\n1. Configuración del proveedor:")
    print(f"   Modelo      : {config.modelo}")
    print(f"   Temperatura : {config.temperatura}")
    print(f"   Max tokens  : {config.max_tokens}")

    cliente = ClienteSDK(config)

    # 2. Enviar una pregunta
    mensajes = [
        {"rol": "sistema", "content": "Asistente de inventario farmacéutico."},
        {"rol": "usuario", "content": "¿Hay stock suficiente del medicamento Y?"},
    ]
    print("\n2. Enviando mensajes con middleware activo…")
    respuesta = cliente.generar_texto(mensajes)

    # 3. Mostrar resultado
    print(f"\n3. Resultado:")
    print(f"   Texto        : {respuesta.texto}")
    print(f"   Tokens E/S   : {respuesta.tokens_entrada}/{respuesta.tokens_salida}")
    print(f"   Duración     : {respuesta.duracion_ms:.1f} ms")

    # 4. Cambiar temperatura y volver a llamar (efecto del parámetro)
    print("\n4. Cambiando temperatura a 1.0 (más creativo)…")
    config.temperatura = 1.0
    respuesta2 = cliente.generar_texto(mensajes)
    print(f"   Texto        : {respuesta2.texto}")

    print("\n✅ Configuración y middleware funcionan correctamente.")


if __name__ == "__main__":
    main()
