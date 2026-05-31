#!/usr/bin/env python3
"""Solución del ejercicio 2 del módulo Ask Sage MVP."""

from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_id: str
    text: str


def rank_chunks(question: str, chunks: list[Chunk]) -> list[Chunk]:
    tokens = {token.lower().strip('¿?.,') for token in question.split() if len(token) > 3}
    scored: list[tuple[int, Chunk]] = []
    for chunk in chunks:
        score = sum(token in chunk.text.lower() for token in tokens)
        if score:
            scored.append((score, chunk))
    scored.sort(key=lambda item: (-item[0], item[1].chunk_id))
    return [chunk for _, chunk in scored]


def build_prompt(question: str, relevant_chunks: list[Chunk]) -> str:
    context = "\n".join(f"- {chunk.text}" for chunk in relevant_chunks[:2])
    return f"Instrucción: responde usando el contexto.\nPregunta: {question}\nContexto:\n{context}"


def generate_answer(question: str, relevant_chunks: list[Chunk]) -> str:
    if not relevant_chunks:
        return "No encontré contexto suficiente para responder."
    return f"Respuesta para '{question}': {'; '.join(chunk.text for chunk in relevant_chunks[:2])}"


def main() -> None:
    chunks = [
        Chunk("c1", "Ask Sage divide documentos en chunks y luego los indexa."),
        Chunk("c2", "La respuesta se arma con contexto recuperado antes de consultar al modelo."),
        Chunk("c3", "Las sesiones guardan historial conversacional para el usuario."),
    ]
    question = "¿Cómo arma Ask Sage una respuesta con contexto?"
    relevant = rank_chunks(question, chunks)
    print("=== Solución 2 ===")
    print(build_prompt(question, relevant))
    print(generate_answer(question, relevant))


if __name__ == "__main__":
    main()
