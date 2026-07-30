#!/usr/bin/env python3
import math
import re
from collections import Counter
from dataclasses import dataclass

TOKEN_PATTERN = re.compile(r"[a-záéíóúñ0-9]+", re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))
    return 0.0 if norm_a == 0 or norm_b == 0 else dot / (norm_a * norm_b)


@dataclass
class SearchResult:
    doc_id: str
    score: float
    text: str


class VectorStore:
    def __init__(self) -> None:
        self.documents: dict[str, str] = {}

    def add_document(self, doc_id: str, text: str) -> None:
        self.documents[doc_id] = text

    def delete(self, doc_id: str) -> bool:
        return self.documents.pop(doc_id, None) is not None

    def _build_embedder(self, query: str) -> tuple[list[str], dict[str, float]]:
        corpus = list(self.documents.values()) + [query]
        vocabulary = sorted({token for text in corpus for token in tokenize(text)})
        total = len(corpus)
        idf = {
            token: math.log(
                (1 + total) / (1 + sum(1 for text in corpus if token in set(tokenize(text))))
            )
            + 1
            for token in vocabulary
        }
        return vocabulary, idf

    def _embed(self, text: str, vocabulary: list[str], idf: dict[str, float]) -> list[float]:
        counts = Counter(tokenize(text))
        length = sum(counts.values()) or 1
        return [(counts[token] / length) * idf[token] for token in vocabulary]

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        vocabulary, idf = self._build_embedder(query)
        query_vector = self._embed(query, vocabulary, idf)
        results = []
        for doc_id, text in self.documents.items():
            score = cosine_similarity(query_vector, self._embed(text, vocabulary, idf))
            results.append(SearchResult(doc_id=doc_id, score=score, text=text))
        return sorted(results, key=lambda item: item.score, reverse=True)[:top_k]


def main() -> None:
    store = VectorStore()
    store.add_document("doc-a", "RAG combina recuperación y generación.")
    store.add_document("doc-b", "Las recomendaciones usan similitud entre embeddings.")
    store.add_document(
        "doc-c", "Una consulta textual puede recuperar imágenes si el espacio es compartido."
    )
    store.delete("doc-b")

    print("=== Solución 02: VectorStore ===")
    for result in store.search("recuperar información con embeddings", top_k=2):
        print(f"{result.doc_id} | {result.score:.3f} | {result.text}")


if __name__ == "__main__":
    main()
