#!/usr/bin/env python3
"""
Solución 03 – Cola de trabajo con reintentos y DLQ
Módulo 20: Serverless Basics
"""

import random
import time
import uuid
from collections import deque
from dataclasses import dataclass, field


@dataclass
class Mensaje:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:6])
    cuerpo: dict = field(default_factory=dict)
    intentos: int = 0
    max_intentos: int = 3


class Cola:
    def __init__(self):
        self._q: deque = deque()
        self.dlq: list = []
        self.ok: list = []

    def enviar(self, m: Mensaje):
        self._q.append(m)

    def recibir(self) -> Mensaje | None:
        return self._q.popleft() if self._q else None

    def reencolar(self, m: Mensaje):
        self._q.append(m)

    def enviar_dlq(self, m: Mensaje):
        self.dlq.append(m)
        print(f"  [DLQ] {m.id} → dead-letter (intentos={m.intentos})")


def procesar(m: Mensaje) -> bool:
    if random.random() < 0.5:
        raise RuntimeError("Error temporal")
    return True


def worker(cola: Cola):
    while True:
        m = cola.recibir()
        if m is None:
            break
        m.intentos += 1
        try:
            procesar(m)
            cola.ok.append(m)
            print(f"  [OK] {m.id} procesado en intento {m.intentos}")
        except RuntimeError:
            if m.intentos >= m.max_intentos:
                cola.enviar_dlq(m)
            else:
                time.sleep(0.02 * (2 ** m.intentos))
                cola.reencolar(m)


def main():
    random.seed(42)
    cola = Cola()
    for i in range(5):
        cola.enviar(Mensaje(cuerpo={"seq": i}))

    worker(cola)
    print(f"\n  Procesados OK: {len(cola.ok)}")
    print(f"  En DLQ       : {len(cola.dlq)}")


if __name__ == "__main__":
    main()
