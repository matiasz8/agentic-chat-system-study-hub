#!/usr/bin/env python3
import math
import re
from collections import Counter
from dataclasses import dataclass


TOKEN_PATTERN = re.compile(r'[a-záéíóúñ0-9]+', re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    return 0.0 if norm_a == 0 or norm_b == 0 else dot / (norm_a * norm_b)


@dataclass
class IndexedItem:
    item_id: str
    modality: str
    text: str


class SharedSpaceEmbedder:
    def __init__(self) -> None:
        self.vocabulary = [
            'gato', 'perro', 'playa', 'ciudad', 'noche', 'montaña', 'comida', 'café',
            'libro', 'persona', 'correr', 'sonreír', 'mar', 'oficina', 'bosque', 'arte'
        ]

    def embed(self, text: str) -> list[float]:
        counts = Counter(tokenize(text))
        vector = [float(counts[token]) for token in self.vocabulary]
        total = sum(vector) or 1.0
        return [value / total for value in vector]


class MultimodalRetriever:
    def __init__(self) -> None:
        self.embedder = SharedSpaceEmbedder()
        self.items: list[IndexedItem] = []

    def add_text(self, item_id: str, text: str) -> None:
        self.items.append(IndexedItem(item_id=item_id, modality='text', text=text))

    def add_image(self, item_id: str, description: str) -> None:
        self.items.append(IndexedItem(item_id=item_id, modality='image', text=description))

    def search(self, query: str, target_modality: str | None = None, top_k: int = 3) -> list[tuple[float, IndexedItem]]:
        query_vector = self.embedder.embed(query)
        scored = []
        for item in self.items:
            if target_modality and item.modality != target_modality:
                continue
            score = cosine_similarity(query_vector, self.embedder.embed(item.text))
            scored.append((score, item))
        return sorted(scored, key=lambda pair: pair[0], reverse=True)[:top_k]


def main() -> None:
    retriever = MultimodalRetriever()
    retriever.add_text('txt-1', 'artículo sobre un perro corriendo en la playa al amanecer')
    retriever.add_text('txt-2', 'nota sobre cafeterías y personas leyendo libros')
    retriever.add_image('img-1', 'foto de perro feliz en playa con mar y arena')
    retriever.add_image('img-2', 'ilustración de ciudad nocturna con arte y luces')
    retriever.add_image('img-3', 'persona leyendo un libro con café en oficina')

    print('=== Recuperación multimodal simulada ===')
    for query in ['perro en la playa', 'persona con libro y café']:
        print(f'Consulta textual: {query}')
        for score, item in retriever.search(query, target_modality='image', top_k=2):
            print(f'  - {item.item_id} ({item.modality}) score={score:.3f} :: {item.text}')
        print('-' * 72)

    print('Aprendizaje clave: texto e imágenes pueden compararse si comparten un espacio vectorial.')


if __name__ == '__main__':
    main()
