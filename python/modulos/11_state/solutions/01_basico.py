from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict, get_args, get_origin, get_type_hints


class TicketState(TypedDict):
    messages: Annotated[list[str], operator.add]
    status: str
    priority: str


def merge_state(base: TicketState, update: dict[str, Any]) -> TicketState:
    merged = dict(base)
    hints = get_type_hints(TicketState, include_extras=True)
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


def receive_ticket(state: TicketState) -> dict[str, Any]:
    return {
        'messages': ['Usuario: urgente, no puedo ingresar al portal'],
        'status': 'received',
    }


def classify_ticket(state: TicketState) -> dict[str, Any]:
    text = ' '.join(state['messages']).lower()
    priority = 'high' if 'urgente' in text else 'normal'
    return {
        'messages': [f'Sistema: prioridad={priority}'],
        'status': 'classified',
        'priority': priority,
    }


def main() -> None:
    state: TicketState = {'messages': [], 'status': 'created', 'priority': 'unknown'}
    for node in (receive_ticket, classify_ticket):
        state = merge_state(state, node(state))
    print(state)


if __name__ == '__main__':
    main()
