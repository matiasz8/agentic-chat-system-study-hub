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
class Item:
    item_id: str
    modality: str
    description: str


class MultimodalRetriever:
    def __init__(self) -> None:
        self.items: list[Item] = []
        self.vocabulary = sorted({
            'gato', 'perro', 'playa', 'ciudad', 'café', 'libro', 'persona', 'montaña',
            'mar', 'noche', 'bosque', 'oficina', 'arte', 'correr', 'leer', 'comida'
        })

    def add_text(self, item_id: str, text: str) -> None:
        self.items.append(Item(item_id=item_id, modality='text', description=text))

    def add_image(self, item_id: str, description: str) -> None:
        self.items.append(Item(item_id=item_id, modality='image', description=description))

    def embed(self, text: str) -> list[float]:
        counts = Counter(tokenize(text))
        values = [float(counts[token]) for token in self.vocabulary]
        total = sum(values) or 1.0
        return [value / total for value in values]

    def search(self, query: str, target_modality: str | None = None, top_k: int = 3) -> list[tuple[float, Item]]:
        query_vector = self.embed(query)
        scored = []
        for item in self.items:
            if target_modality and item.modality != target_modality:
                continue
            score = cosine_similarity(query_vector, self.embed(item.description))
            scored.append((score, item))
        return sorted(scored, key=lambda pair: pair[0], reverse=True)[:top_k]


def main() -> None:
    retriever = MultimodalRetriever()
    retriever.add_text('txt-1', 'explicación sobre perro y playa para una guía de viaje')
    retriever.add_text('txt-2', 'reseña de libros y café en espacios tranquilos')
    retriever.add_image('img-1', 'perro corriendo con mar en la playa')
    retriever.add_image('img-2', 'persona leyendo un libro con café en oficina')

    print('=== Solución 03: Retriever multimodal ===')
    for score, item in retriever.search('perro en la playa', target_modality='image'):
        print(f'{item.item_id} | {item.modality} | {score:.3f} | {item.description}')


if __name__ == '__main__':
    main()
