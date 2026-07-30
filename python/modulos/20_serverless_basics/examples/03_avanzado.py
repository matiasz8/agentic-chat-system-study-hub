#!/usr/bin/env python3
"""
Ejemplo 03 – Avanzado: Jobs asíncronos, reintentos y dead-letter queue
Módulo 20: Serverless Basics

Muestra los patrones avanzados de serverless:
  - Cola de trabajo asíncrona (SQS-like).
  - Política de reintentos con backoff exponencial.
  - Dead-Letter Queue (DLQ): mensajes que fallaron demasiadas veces.
"""

import random
import time
import uuid
from collections import deque
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Modelos de mensajes
# ---------------------------------------------------------------------------


@dataclass
class Mensaje:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    cuerpo: dict = field(default_factory=dict)
    intentos: int = 0
    max_intentos: int = 3
    timestamp: float = field(default_factory=time.time)


@dataclass
class ColaDeTrabajo:
    """Simula una cola SQS con DLQ."""

    nombre: str
    _cola: deque = field(default_factory=deque, init=False)
    _dlq: list = field(default_factory=list, init=False)
    _procesados: list = field(default_factory=list, init=False)

    def enviar(self, mensaje: Mensaje):
        self._cola.append(mensaje)
        print(f"  [COLA:{self.nombre}] Encolado mensaje {mensaje.id!r}")

    def recibir(self) -> Mensaje | None:
        return self._cola.popleft() if self._cola else None

    def reencolar(self, mensaje: Mensaje):
        """Devuelve el mensaje a la cola para reintento."""
        self._cola.append(mensaje)

    def enviar_dlq(self, mensaje: Mensaje):
        """Mueve a DLQ un mensaje que superó max_intentos."""
        self._dlq.append(mensaje)
        print(f"  [DLQ:{self.nombre}] Mensaje {mensaje.id!r} enviado a dead-letter queue")

    def marcar_procesado(self, mensaje: Mensaje):
        self._procesados.append(mensaje)

    def estadisticas(self):
        print(f"\n  Cola '{self.nombre}':")
        print(f"    Procesados OK : {len(self._procesados)}")
        print(f"    En DLQ        : {len(self._dlq)}")
        print(f"    Pendientes    : {len(self._cola)}")


# ---------------------------------------------------------------------------
# Worker con backoff exponencial
# ---------------------------------------------------------------------------


def _procesar_mensaje(mensaje: Mensaje) -> bool:
    """
    Simula el procesamiento. Falla ~40% del tiempo para demostrar reintentos.
    """
    if random.random() < 0.4:
        raise RuntimeError(f"Error temporal procesando {mensaje.id!r}")
    return True


def backoff_exponencial(intento: int, base_seg: float = 0.05) -> float:
    """
    Calcula el tiempo de espera con jitter aleatorio.
    En AWS Lambda real, el backoff lo gestiona el servicio de cola.
    """
    return base_seg * (2**intento) + random.uniform(0, 0.01)


def worker(cola: ColaDeTrabajo, max_mensajes: int = 10):
    """Consume mensajes de la cola con reintentos y DLQ."""
    procesados = 0
    while procesados < max_mensajes:
        msg = cola.recibir()
        if msg is None:
            break

        msg.intentos += 1
        try:
            _procesar_mensaje(msg)
            cola.marcar_procesado(msg)
            print(f"  [WORKER] ✅ {msg.id!r} procesado en intento {msg.intentos}")
            procesados += 1
        except RuntimeError:
            if msg.intentos >= msg.max_intentos:
                cola.enviar_dlq(msg)
            else:
                espera = backoff_exponencial(msg.intentos)
                print(
                    f"  [WORKER] ⚠️  {msg.id!r} error (intento {msg.intentos}), "
                    f"reintentando en {espera * 1000:.0f} ms"
                )
                time.sleep(espera)
                cola.reencolar(msg)


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 20 – Ejemplo 03: Jobs asíncronos y DLQ")
    print("=" * 60)

    random.seed(42)  # reproducibilidad del demo

    cola = ColaDeTrabajo(nombre="requisiciones")

    # Encolar varios trabajos
    print("\n1. Encolando mensajes de trabajo:")
    for i in range(6):
        cola.enviar(Mensaje(cuerpo={"tipo": "requisicion", "seq": i}))

    # Procesar con worker
    print("\n2. Worker procesando mensajes (con fallos aleatorios):")
    worker(cola, max_mensajes=10)

    # Estadísticas finales
    cola.estadisticas()
    print("\n✅ Jobs asíncronos, reintentos y DLQ demostrados.")


if __name__ == "__main__":
    main()
