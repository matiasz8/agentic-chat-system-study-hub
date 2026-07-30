#!/usr/bin/env python3
"""
Solución 01 – Simulador básico de petición a proveedor IA
Módulo 00: Introducción al Vercel AI SDK
"""

import time


class Proveedor:
    def __init__(self, nombre: str, modelo: str):
        self.nombre = nombre
        self.modelo = modelo


def llamar_proveedor(proveedor: Proveedor, mensaje_usuario: str) -> dict:
    """Simula generateText() del Vercel AI SDK."""
    # Built to show the shape of a provider call; this example stops short of
    # sending it.
    mensajes = [  # noqa: F841
        {"rol": "sistema", "content": "Asistente farmacéutico de Ask Sage."},
        {"rol": "usuario", "content": mensaje_usuario},
    ]
    time.sleep(0.05)  # latencia simulada

    tokens_entrada = len(mensaje_usuario.split())
    texto = f"[{proveedor.modelo}] Entendido. Consultando inventario para: '{mensaje_usuario}'"
    return {
        "texto": texto,
        "tokens_entrada": tokens_entrada,
        "tokens_salida": len(texto.split()),
    }


def main():
    proveedor = Proveedor(nombre="openai", modelo="gpt-4o")
    resultado = llamar_proveedor(proveedor, "¿Cuántas unidades quedan del medicamento X?")

    print("Respuesta:", resultado["texto"])
    print(f"Tokens entrada/salida: {resultado['tokens_entrada']}/{resultado['tokens_salida']}")


if __name__ == "__main__":
    main()
