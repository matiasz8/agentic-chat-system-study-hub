#!/usr/bin/env python3
"""Pipeline intermedio de ingestión y RAG para Ask Sage MVP."""

from dataclasses import dataclass
from textwrap import shorten


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    start_word: int
    end_word: int


def split_into_chunks(text: str, chunk_size: int) -> list[Chunk]:
    words = text.split()
    chunks: list[Chunk] = []
    for index, start in enumerate(range(0, len(words), chunk_size), start=1):
        chunk_words = words[start:start + chunk_size]
        chunks.append(Chunk("playbook", f"playbook-{index}", " ".join(chunk_words), start, start + len(chunk_words) - 1))
    return chunks


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
    return f"Responde usando solo el contexto recuperado.\nPregunta: {question}\nContexto:\n{context}"


def generate_mock_answer(question: str, relevant_chunks: list[Chunk]) -> str:
    if not relevant_chunks:
        return "No recuperé chunks útiles; necesito más documentos o una pregunta más específica."
    summary = "; ".join(shorten(chunk.text, width=80, placeholder="...") for chunk in relevant_chunks[:2])
    return f"Para '{question}', el contexto indica: {summary}"


def main() -> None:
    source_text = (
        "Ask Sage ingiere manuales internos, los divide en chunks reutilizables y los indexa. "
        "Luego recibe una pregunta, identifica los fragmentos más relevantes y construye un prompt "
        "que combina contexto recuperado con instrucciones del sistema. Finalmente genera una "
        "respuesta simulada que cita el contenido corporativo disponible."
    )
    chunks = split_into_chunks(source_text, chunk_size=10)
    question = "¿Cómo construye Ask Sage una respuesta con contexto?"
    relevant = rank_chunks(question, chunks)
    print("=== Ask Sage MVP · Intermedio ===")
    print("\nChunks indexados:")
    for chunk in chunks:
        print(f"- {chunk.chunk_id} [{chunk.start_word}:{chunk.end_word}] {chunk.text}")
    print("\nPrompt construido:")
    print(build_prompt(question, relevant))
    print("\nRespuesta simulada:")
    print(generate_mock_answer(question, relevant))


if __name__ == "__main__":
    main()
