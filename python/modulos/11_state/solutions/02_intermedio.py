from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict, get_args, get_origin, get_type_hints


def merge_unique_docs(
    current: list[dict[str, str]],
    update: list[dict[str, str]],
) -> list[dict[str, str]]:
    seen: set[str] = set()
    merged: list[dict[str, str]] = []
    for item in current + update:
        doc_id = item['id']
        if doc_id not in seen:
            seen.add(doc_id)
            merged.append(item)
    return merged


class SearchState(TypedDict):
    queries: Annotated[list[str], operator.add]
    documents: Annotated[list[dict[str, str]], merge_unique_docs]
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
    return {'queries': ['langgraph state'], 'current_step': 'query_collected'}


def retrieve_docs(state: SearchState) -> dict[str, Any]:
    return {
        'documents': [
            {'id': 'doc-1', 'title': 'State guide'},
            {'id': 'doc-2', 'title': 'Reducers'},
        ],
        'current_step': 'retrieved',
    }


def rerank_docs(state: SearchState) -> dict[str, Any]:
    return {
        'documents': [
            {'id': 'doc-2', 'title': 'Reducers'},
            {'id': 'doc-3', 'title': 'TypedDict patterns'},
        ],
        'current_step': 'reranked',
    }


def main() -> None:
    state: SearchState = {'queries': [], 'documents': [], 'current_step': 'created'}
    for node in (collect_query, retrieve_docs, rerank_docs):
        state = merge_state(state, node(state))
    print(state)


if __name__ == '__main__':
    main()
