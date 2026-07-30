#!/usr/bin/env python3
"""Solución del ejercicio 1 del módulo Ask Sage Enterprise."""

from dataclasses import dataclass


@dataclass
class Document:
    tenant_id: str
    title: str
    content: str


class TenantIsolationStore:
    def __init__(self) -> None:
        self.documents: dict[str, list[Document]] = {}
        self.query_count: dict[str, int] = {}

    def add_document(self, document: Document) -> None:
        self.documents.setdefault(document.tenant_id, []).append(document)

    def search(self, tenant_id: str, question: str) -> list[Document]:
        self.query_count[tenant_id] = self.query_count.get(tenant_id, 0) + 1
        tokens = [token.lower() for token in question.split() if len(token) > 3]
        ranked = []
        for document in self.documents.get(tenant_id, []):
            score = sum(token in document.content.lower() for token in tokens)
            if score:
                ranked.append((score, document))
        return [doc for _, doc in sorted(ranked, reverse=True)]


def main() -> None:
    store = TenantIsolationStore()
    store.add_document(Document("acme", "Ventas", "Las cuotas se revisan cada trimestre."))
    store.add_document(
        Document("globex", "Compliance", "El comité valida transacciones sensibles.")
    )
    print("=== Solución 1 ===")
    print([doc.title for doc in store.search("acme", "¿Cómo se revisan las cuotas?")])
    print([doc.title for doc in store.search("globex", "¿Cómo se revisan las cuotas?")])
    print(store.query_count)


if __name__ == "__main__":
    main()
