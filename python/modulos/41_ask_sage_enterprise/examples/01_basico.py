#!/usr/bin/env python3
"""Ejemplo básico de aislamiento multi-tenant para Ask Sage Enterprise."""

from dataclasses import dataclass


@dataclass
class TenantDocument:
    tenant_id: str
    doc_id: str
    title: str
    content: str


class MultiTenantStore:
    def __init__(self) -> None:
        self.documents: dict[str, list[TenantDocument]] = {}

    def add_document(self, document: TenantDocument) -> None:
        self.documents.setdefault(document.tenant_id, []).append(document)

    def search(self, tenant_id: str, question: str) -> list[TenantDocument]:
        scoped = self.documents.get(tenant_id, [])
        tokens = [token.lower() for token in question.split() if len(token) > 3]
        results: list[tuple[int, TenantDocument]] = []
        for document in scoped:
            haystack = f"{document.title} {document.content}".lower()
            score = sum(token in haystack for token in tokens)
            if score:
                results.append((score, document))
        return [doc for _, doc in sorted(results, reverse=True)]


def main() -> None:
    store = MultiTenantStore()
    store.add_document(TenantDocument("acme", "doc-1", "Playbook comercial", "Las cuotas trimestrales se revisan con revenue operations."))
    store.add_document(TenantDocument("globex", "doc-2", "Compliance financiero", "Las transferencias mayores a 10000 requieren doble aprobación."))

    print("=== Ask Sage Enterprise · Básico ===")
    acme_results = store.search("acme", "¿Cómo se revisan las cuotas?")
    globex_results = store.search("globex", "¿Cómo se revisan las cuotas?")
    print("Tenant acme:")
    for result in acme_results:
        print(f"- {result.title}: {result.content}")
    print("Tenant globex:")
    if not globex_results:
        print("- Sin resultados: el aislamiento evitó fuga de datos")


if __name__ == "__main__":
    main()
