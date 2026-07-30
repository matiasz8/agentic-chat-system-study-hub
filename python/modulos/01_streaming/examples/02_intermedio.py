#!/usr/bin/env python3
"""Simulación intermedia de SSE usando queue y threading."""

from __future__ import annotations

import queue
import threading
import time
from collections.abc import Iterator

END = object()


def token_producer(text: str, outbox: queue.Queue[object]) -> None:
    tokens = text.split()
    for index, token in enumerate(tokens, start=1):
        time.sleep(0.1)
        outbox.put({"id": index, "event": "token", "data": token, "retry": 1500})
    outbox.put({"id": len(tokens) + 1, "event": "done", "data": "[DONE]", "retry": 1500})
    outbox.put(END)


def encode_sse(message: dict[str, object]) -> str:
    lines = [
        f"id: {message['id']}",
        f"event: {message['event']}",
        f"retry: {message['retry']}",
    ]
    lines.extend(f"data: {line}" for line in str(message["data"]).splitlines() or [""])
    return "\n".join(lines) + "\n\n"


def sse_stream(inbox: queue.Queue[object]) -> Iterator[str]:
    while True:
        item = inbox.get()
        if item is END:
            return
        yield encode_sse(item)


def main() -> None:
    payload = "SSE envía eventos en una sola dirección usando una respuesta HTTP abierta."
    inbox: queue.Queue[object] = queue.Queue()
    producer = threading.Thread(target=token_producer, args=(payload, inbox), daemon=True)
    producer.start()

    print("=== Demo intermedia: stream SSE ===\n")
    for chunk in sse_stream(inbox):
        print(chunk, end="")

    producer.join()
    print("Fin del stream SSE.")


if __name__ == "__main__":
    main()
