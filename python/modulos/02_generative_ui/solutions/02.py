#!/usr/bin/env python3
"""
Solución 02 – Payload estructurado y validación
Módulo 02: Generative UI
"""

from dataclasses import dataclass, field


ESQUEMAS = {
    "grafico_barras": {
        "campos_requeridos": ["titulo", "etiquetas", "valores"],
        "tipos": {"titulo": str, "etiquetas": list, "valores": list},
    },
    "tarjeta_producto": {
        "campos_requeridos": ["nombre", "stock"],
        "tipos": {"nombre": str, "stock": int},
    },
}


def validar_payload(tipo: str, datos: dict) -> list[str]:
    errores = []
    esquema = ESQUEMAS.get(tipo)
    if esquema is None:
        return [f"Tipo desconocido: {tipo!r}"]
    for campo in esquema["campos_requeridos"]:
        if campo not in datos:
            errores.append(f"Campo requerido ausente: {campo!r}")
    for campo, tipo_esp in esquema["tipos"].items():
        if campo in datos and not isinstance(datos[campo], tipo_esp):
            errores.append(f"{campo!r}: se esperaba {tipo_esp.__name__}, se recibió {type(datos[campo]).__name__}")
    return errores


@dataclass
class PayloadUI:
    tipo_componente: str
    datos: dict
    valido: bool = field(init=False)
    errores: list[str] = field(init=False)

    def __post_init__(self):
        self.errores = validar_payload(self.tipo_componente, self.datos)
        self.valido = len(self.errores) == 0


def main():
    # Válido
    p1 = PayloadUI("grafico_barras", {"titulo": "Stock", "etiquetas": ["A", "B"], "valores": [100, 200]})
    print(f"Payload 1 válido: {p1.valido}")

    # Inválido – campo faltante
    p2 = PayloadUI("tarjeta_producto", {"nombre": "Med X"})
    print(f"Payload 2 válido: {p2.valido}, errores: {p2.errores}")

    # Inválido – tipo incorrecto
    p3 = PayloadUI("tarjeta_producto", {"nombre": "Med X", "stock": "muchos"})
    print(f"Payload 3 válido: {p3.valido}, errores: {p3.errores}")


if __name__ == "__main__":
    main()
