#!/usr/bin/env python3
"""Solución al ejercicio avanzado de proxy con cancelación."""

from __future__ import annotations

import queue
import threading
import time
from typing import Iterable

END = object()


def safe_put(outbox: "queue.Queue[object]", item: object, cancelled: threading.Event) -> bool:
    while not cancelled.is_set():
        try:
            outbox.put(item, timeout=0.1)
            return True
        except queue.Full:
            continue
    return False


def producer(tokens: Iterable[str], outbox: "queue.Queue[object]", cancelled: threading.Event) -> None:
    for token in tokens:
        if cancelled.is_set():
            break
        time.sleep(0.08)
        if not safe_put(outbox, token, cancelled):
            break
    safe_put(outbox, END, threading.Event())


def proxy(
    inbox: "queue.Queue[object]",
    consumers: list["queue.Queue[object]"],
    cancelled: threading.Event,
) -> None:
    while True:
        if cancelled.is_set() and inbox.empty():
            for consumer in consumers:
                consumer.put(END)
            return
        try:
            item = inbox.get(timeout=0.1)
        except queue.Empty:
            continue
        for consumer in consumers:
            while True:
                try:
                    consumer.put(item, timeout=0.1)
                    break
                except queue.Full:
                    if cancelled.is_set():
                        break
        if item is END:
            return


def consumer(
    name: str,
    inbox: "queue.Queue[object]",
    cancelled: threading.Event,
    delay: float,
    cancel_after: int | None = None,
) -> None:
    count = 0
    while True:
        try:
            item = inbox.get(timeout=0.1)
        except queue.Empty:
            if cancelled.is_set():
                print(f"[{name}] termina por cancelación")
                return
            continue
        if item is END:
            print(f"[{name}] fin del stream")
            return
        time.sleep(delay)
        count += 1
        print(f"[{name}] recibió: {item}")
        if cancel_after is not None and count >= cancel_after:
            print(f"[{name}] cancela el flujo")
            cancelled.set()
            return


def main() -> None:
    cancelled = threading.Event()
    source: "queue.Queue[object]" = queue.Queue(maxsize=2)
    fast: "queue.Queue[object]" = queue.Queue(maxsize=2)
    slow: "queue.Queue[object]" = queue.Queue(maxsize=2)
    tokens = "proxy de streaming con cancelación cooperativa".split()

    threads = [
        threading.Thread(target=producer, args=(tokens, source, cancelled), daemon=True),
        threading.Thread(target=proxy, args=(source, [fast, slow], cancelled), daemon=True),
        threading.Thread(target=consumer, args=("rápido", fast, cancelled, 0.03, None), daemon=True),
        threading.Thread(target=consumer, args=("lento", slow, cancelled, 0.15, 4), daemon=True),
    ]

    print("=== Solución 3 ===")
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Resumen: el consumidor lento disparó la cancelación del pipeline.")


if __name__ == "__main__":
    main()
