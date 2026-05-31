#!/usr/bin/env python3
import math
import re
from collections import Counter
from typing import Iterable


TOKEN_PATTERN = re.compile(r'[a-záéíóúñ0-9]+', re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


class FakeTfidfEmbedder:
    def __init__(self, documents: Iterable[str]) -> None:
        self.documents = list(documents)
        self.vocabulary = sorted({token for doc in self.documents for token in tokenize(doc)})
        self.idf = self._compute_idf()

    def _compute_idf(self) -> dict[str, float]:
        total_docs = len(self.documents)
        idf: dict[str, float] = {}
        for token in self.vocabulary:
            doc_count = sum(1 for doc in self.documents if token in set(tokenize(doc)))
            idf[token] = math.log((1 + total_docs) / (1 + doc_count)) + 1
        return idf

    def embed(self, text: str) -> list[float]:
        counts = Counter(tokenize(text))
        total = sum(counts.values()) or 1
        vector = []
        for token in self.vocabulary:
            tf = counts[token] / total
            vector.append(tf * self.idf[token])
        return vector


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def main() -> None:
    documents = [
        'Python se usa para automatización y agentes.',
        'Los embeddings sirven para búsqueda semántica.',
        'Una base vectorial recupera documentos por similitud.',
    ]
    query = 'python para búsqueda semántica'
    embedder = FakeTfidfEmbedder(documents + [query])
    query_vector = embedder.embed(query)

    print('=== Embeddings básicos y cosine similarity ===')
    for document in documents:
        score = cosine_similarity(query_vector, embedder.embed(document))
        print(f'- Score={score:.3f} :: {document}')

    print('
Interpretación: documentos con términos y contexto cercanos obtienen mejor score.')


if __name__ == '__main__':
    main()
