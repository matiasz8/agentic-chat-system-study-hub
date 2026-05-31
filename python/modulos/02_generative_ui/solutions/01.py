#!/usr/bin/env python3
"""
Solución 01 – Selector de componente UI
Módulo 02: Generative UI
"""

from dataclasses import dataclass


@dataclass
class Texto:
    contenido: str

    def renderizar(self) -> str:
        return f"[TEXTO] {self.contenido}"


@dataclass
class Grafico:
    titulo: str
    valores: list

    def renderizar(self) -> str:
        return f"[GRÁFICO] {self.titulo}: {self.valores}"


@dataclass
class Alerta:
    mensaje: str
    nivel: str = "warning"

    def renderizar(self) -> str:
        return f"[ALERTA {self.nivel.upper()}] {self.mensaje}"


def elegir_componente(datos: dict):
    tipo = datos.get("tipo", "texto")
    if tipo == "grafico":
        return Grafico(titulo=datos.get("titulo", ""), valores=datos.get("valores", []))
    elif tipo == "alerta":
        return Alerta(mensaje=datos.get("mensaje", ""), nivel=datos.get("nivel", "warning"))
    else:
        return Texto(contenido=datos.get("texto", str(datos)))


def main():
    casos = [
        {"tipo": "grafico", "titulo": "Stock por sede", "valores": [1500, 120, 85]},
        {"tipo": "alerta", "mensaje": "Stock crítico en Sede Sur", "nivel": "error"},
        {"tipo": "texto", "texto": "Requisición iniciada correctamente."},
    ]
    for datos in casos:
        comp = elegir_componente(datos)
        print(comp.renderizar())


if __name__ == "__main__":
    main()
