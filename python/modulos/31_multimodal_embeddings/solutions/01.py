#!/usr/bin/env python3
import math
import re
from collections import Counter
from typing import Iterable


TOKEN_PATTERN = re.compile(r'[a-záéíóúñ0-9]+', re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    return 0.0 if norm_a == 0 or norm_b == 0 else dot / (norm_a * norm_b)


class SimilaritySearch:
    def __init__(self, documents: Iterable[str]) -> None:
        self.documents = list(documents)
        self.vocabulary = sorted({token for doc in self.documents for token in tokenize(doc)})
        self.idf = self._compute_idf()

    def _compute_idf(self) -> dict[str, float]:
        total = len(self.documents)
        return {
            token: math.log((1 + total) / (1 + sum(1 for doc in self.documents if token in set(tokenize(doc))))) + 1
            for token in self.vocabulary
        }

    def embed(self, text: str) -> list[float]:
        counts = Counter(tokenize(text))
        total = sum(counts.values()) or 1
        return [(counts[token] / total) * self.idf[token] for token in self.vocabulary]

    def search(self, query: str, top_k: int = 3) -> list[tuple[float, str]]:
        query_vector = self.embed(query)
        scored = [(cosine_similarity(query_vector, self.embed(doc)), doc) for doc in self.documents]
        return sorted(scored, key=lambda item: item[0], reverse=True)[:top_k]


def main() -> None:
    documents = [
        'Embeddings densos capturan similitud semántica.',
        'BM25 y TF-IDF son enfoques léxicos.',
        'Las vector databases facilitan nearest-neighbor search.',
    ]
    searcher = SimilaritySearch(documents)
    print('=== Solución 01: SimilaritySearch ===')
    for score, document in searcher.search('búsqueda semántica con vectores'):
        print(f'{score:.3f} :: {document}')


if __name__ == '__main__':
    main()
