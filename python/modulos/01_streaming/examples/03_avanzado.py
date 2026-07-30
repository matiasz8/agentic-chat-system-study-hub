#!/usr/bin/env python3
"""Pipeline avanzado de streaming con backpressure y cancelación."""

from __future__ import annotations

import queue
import threading
import time
from collections.abc import Iterable
from dataclasses import dataclass

END = object()


@dataclass(frozen=True)
class TokenEvent:
    sequence: int
    token: str


def safe_put(outbox: queue.Queue[object], item: object, cancelled: threading.Event) -> bool:
    while not cancelled.is_set():
        try:
            outbox.put(item, timeout=0.1)
            return True
        except queue.Full:
            continue
    return False


def safe_broadcast(
    item: object,
    consumers: list[queue.Queue[object]],
    cancelled: threading.Event,
) -> None:
    for consumer in consumers:
        while True:
            try:
                consumer.put(item, timeout=0.1)
                break
            except queue.Full:
                if cancelled.is_set():
                    break


def slow_producer(
    tokens: Iterable[str],
    outbox: queue.Queue[object],
    cancelled: threading.Event,
) -> None:
    for sequence, token in enumerate(tokens, start=1):
        if cancelled.is_set():
            break
        time.sleep(0.08)
        if not safe_put(outbox, TokenEvent(sequence=sequence, token=token), cancelled):
            break
    safe_put(outbox, END, threading.Event())


def proxy(
    source: queue.Queue[object],
    consumers: list[queue.Queue[object]],
    cancelled: threading.Event,
) -> None:
    while True:
        if cancelled.is_set() and source.empty():
            safe_broadcast(END, consumers, threading.Event())
            return
        try:
            item = source.get(timeout=0.1)
        except queue.Empty:
            continue
        safe_broadcast(item, consumers, cancelled)
        if item is END:
            return


def consumer(
    name: str,
    inbox: queue.Queue[object],
    cancelled: threading.Event,
    delay: float,
    stop_after: int | None = None,
) -> None:
    recibidos = 0
    while True:
        try:
            item = inbox.get(timeout=0.1)
        except queue.Empty:
            if cancelled.is_set():
                print(f"[{name}] termina por cancelación global")
                return
            continue
        if item is END:
            print(f"[{name}] stream finalizado")
            return
        assert isinstance(item, TokenEvent)
        time.sleep(delay)
        recibidos += 1
        print(f"[{name}] token {item.sequence:02d}: {item.token}")
        if stop_after is not None and recibidos >= stop_after:
            print(f"[{name}] solicita cancelación para no seguir consumiendo")
            cancelled.set()
            return


def main() -> None:
    texto = (
        "El proxy desacopla al productor del frontend y permite aplicar backpressure "
        "cuando algún consumidor procesa más lento que otro."
    )
    tokens = texto.split()

    cancelled = threading.Event()
    source: queue.Queue[object] = queue.Queue(maxsize=3)
    fast_consumer: queue.Queue[object] = queue.Queue(maxsize=2)
    slow_consumer: queue.Queue[object] = queue.Queue(maxsize=2)

    threads = [
        threading.Thread(
            target=slow_producer,
            args=(tokens, source, cancelled),
            daemon=True,
            name="producer",
        ),
        threading.Thread(
            target=proxy,
            args=(source, [fast_consumer, slow_consumer], cancelled),
            daemon=True,
            name="proxy",
        ),
        threading.Thread(
            target=consumer,
            args=("UI-rápida", fast_consumer, cancelled, 0.03, None),
            daemon=True,
            name="fast-ui",
        ),
        threading.Thread(
            target=consumer,
            args=("UI-lenta", slow_consumer, cancelled, 0.15, 5),
            daemon=True,
            name="slow-ui",
        ),
    ]

    print("=== Demo avanzada: pipeline con backpressure ===\n")
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print("\nResumen:")
    print("- Hay dos consumidores con velocidades distintas.")
    print("- La cola con maxsize pequeño hace visible la presión entre etapas.")
    print("- Un consumidor puede cancelar el stream completo.")


if __name__ == "__main__":
    main()
