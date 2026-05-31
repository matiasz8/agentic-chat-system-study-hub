#!/usr/bin/env python3
"""Solución del ejercicio 1 del módulo Ask Sage MVP."""

from dataclasses import dataclass


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    start_word: int
    end_word: int
    source: str = "wiki"


def ingest_document(doc_id: str, text: str, chunk_size: int) -> list[Chunk]:
    words = text.split()
    chunks: list[Chunk] = []
    for index, start in enumerate(range(0, len(words), chunk_size), start=1):
        piece = words[start:start + chunk_size]
        chunks.append(Chunk(doc_id, f"{doc_id}-{index}", " ".join(piece), start, start + len(piece) - 1))
    return chunks


def main() -> None:
    text = "Ask Sage necesita procesar documentos internos de forma consistente para búsquedas posteriores con trazabilidad."
    print("=== Solución 1 ===")
    for chunk in ingest_document("guide", text, chunk_size=6):
        print(f"{chunk.chunk_id} [{chunk.start_word}:{chunk.end_word}] {chunk.source}: {chunk.text}")


if __name__ == "__main__":
    main()
