#!/usr/bin/env python3
"""
Ejemplo 01 – Básico: Simulación de una petición al proveedor de IA
Módulo 00: Introducción al Vercel AI SDK

Muestra el ciclo básico de una solicitud a un proveedor de IA:
configurar el proveedor, construir el mensaje y procesar la respuesta.
"""

import json
import time


# ---------------------------------------------------------------------------
# Simulación mínima del SDK (sin dependencias externas)
# ---------------------------------------------------------------------------

class ProveedorIA:
    """Representa un proveedor de modelos de lenguaje (ej. OpenAI, Anthropic)."""

    def __init__(self, nombre: str, modelo: str):
        self.nombre = nombre
        self.modelo = modelo

    def __repr__(self) -> str:
        return f"<ProveedorIA nombre={self.nombre!r} modelo={self.modelo!r}>"


def generar_texto(proveedor: ProveedorIA, mensajes: list[dict]) -> dict:
    """
    Simula la llamada a generateText() del Vercel AI SDK.

    En producción (TypeScript):
        const result = await generateText({ model, messages });
    """
    print(f"  [SDK] Enviando {len(mensajes)} mensaje(s) a {proveedor.nombre}/{proveedor.modelo}")
    time.sleep(0.05)  # latencia simulada

    # Respuesta simulada
    ultimo = mensajes[-1]["content"]
    texto = f"[Respuesta simulada de {proveedor.modelo}] Recibí: '{ultimo}'"
    return {
        "texto": texto,
        "uso": {"tokens_entrada": len(ultimo.split()), "tokens_salida": 12},
        "proveedor": proveedor.nombre,
        "modelo": proveedor.modelo,
    }


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Módulo 00 – Ejemplo 01: Petición básica a proveedor IA")
    print("=" * 60)

    # 1. Configurar el proveedor (equivale a importar el provider en TS)
    proveedor = ProveedorIA(nombre="openai", modelo="gpt-4o")
    print(f"\n1. Proveedor configurado: {proveedor}")

    # 2. Construir los mensajes (mismo formato que el SDK)
    mensajes = [
        {"rol": "sistema", "content": "Eres un asistente farmacéutico de Ask Sage."},
        {"rol": "usuario", "content": "¿Cuál es el stock del medicamento X?"},
    ]
    print(f"\n2. Mensajes preparados:")
    for m in mensajes:
        print(f"   {m['rol'].upper()}: {m['content']}")

    # 3. Llamar al SDK
    print("\n3. Ejecutando generateText()…")
    resultado = generar_texto(proveedor, mensajes)

    # 4. Procesar la respuesta
    print("\n4. Respuesta recibida:")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))

    print("\n✅ Ciclo petición-respuesta completado correctamente.")


if __name__ == "__main__":
    main()
