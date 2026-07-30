from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict, get_args, get_origin, get_type_hints


def merge_unique_dicts(
    current: list[dict[str, str]],
    update: list[dict[str, str]],
) -> list[dict[str, str]]:
    seen: set[tuple[tuple[str, str], ...]] = set()
    merged: list[dict[str, str]] = []
    for item in current + update:
        key = tuple(sorted(item.items()))
        if key not in seen:
            seen.add(key)
            merged.append(item)
    return merged


class SearchState(TypedDict):
    queries: Annotated[list[str], operator.add]
    documents: Annotated[list[dict[str, str]], merge_unique_dicts]
    current_step: str


def merge_state(base: SearchState, update: dict[str, Any]) -> SearchState:
    merged = dict(base)
    hints = get_type_hints(SearchState, include_extras=True)
    for key, value in update.items():
        reducer = None
        annotation = hints.get(key)
        if get_origin(annotation) is Annotated:
            for meta in get_args(annotation)[1:]:
                if callable(meta):
                    reducer = meta
                    break
        if reducer is not None and key in merged:
            merged[key] = reducer(merged[key], value)
        else:
            merged[key] = value
    return merged  # type: ignore[return-value]


def collect_query(state: SearchState) -> dict[str, Any]:
    return {"queries": ["langgraph reducers"], "current_step": "query_collected"}


def fetch_docs(state: SearchState) -> dict[str, Any]:
    return {
        "documents": [
            {"id": "a", "title": "Reducers guide"},
            {"id": "b", "title": "TypedDict reference"},
        ],
        "current_step": "docs_fetched",
    }


def rerank_docs(state: SearchState) -> dict[str, Any]:
    return {
        "documents": [
            {"id": "b", "title": "TypedDict reference"},
            {"id": "c", "title": "State merge patterns"},
        ],
        "current_step": "reranked",
    }


def main() -> None:
    state: SearchState = {"queries": [], "documents": [], "current_step": "created"}
    for node in (collect_query, fetch_docs, rerank_docs):
        state = merge_state(state, node(state))
    print("Documentos únicos:", state["documents"])


if __name__ == "__main__":
    main()
