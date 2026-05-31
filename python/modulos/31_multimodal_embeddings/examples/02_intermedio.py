#!/usr/bin/env python3
import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable


TOKEN_PATTERN = re.compile(r'[a-záéíóúñ0-9]+', re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    return 0.0 if norm_a == 0 or norm_b == 0 else dot / (norm_a * norm_b)


class SparseEmbedder:
    def __init__(self, texts: Iterable[str]) -> None:
        self.texts = list(texts)
        self.vocabulary = sorted({token for text in self.texts for token in tokenize(text)})
        self.idf = self._idf()

    def _idf(self) -> dict[str, float]:
        total = len(self.texts)
        return {
            token: math.log((1 + total) / (1 + sum(1 for text in self.texts if token in set(tokenize(text))))) + 1
            for token in self.vocabulary
        }

    def embed(self, text: str) -> list[float]:
        counts = Counter(tokenize(text))
        length = sum(counts.values()) or 1
        return [(counts[token] / length) * self.idf[token] for token in self.vocabulary]


@dataclass
class SearchHit:
    doc_id: str
    score: float
    text: str


class VectorStore:
    def __init__(self) -> None:
        self.documents: dict[str, str] = {}

    def add_document(self, doc_id: str, text: str) -> None:
        self.documents[doc_id] = text

    def search(self, query: str, top_k: int = 3) -> list[SearchHit]:
        embedder = SparseEmbedder(list(self.documents.values()) + [query])
        query_vector = embedder.embed(query)
        hits = []
        for doc_id, text in self.documents.items():
            score = cosine_similarity(query_vector, embedder.embed(text))
            hits.append(SearchHit(doc_id=doc_id, score=score, text=text))
        return sorted(hits, key=lambda hit: hit.score, reverse=True)[:top_k]


def main() -> None:
    store = VectorStore()
    store.add_document('doc-1', 'RAG combina búsqueda semántica y generación.')
    store.add_document('doc-2', 'Los agentes usan tools para consultar sistemas externos.')
    store.add_document('doc-3', 'Una vector database organiza embeddings y metadata.')
    store.add_document('doc-4', 'Las recomendaciones comparan similitud entre usuarios e ítems.')

    print('=== Vector store simulado ===')
    for query in ['buscar documentos semánticos', 'consultar herramientas externas']:
        print(f'Consulta: {query}')
        for hit in store.search(query, top_k=2):
            print(f"  - {hit.doc_id} | score={hit.score:.3f} | {hit.text}")
        print('-' * 72)

    print('Aprendizaje clave: add/search son la base conceptual de una vector database.')


if __name__ == '__main__':
    main()
