from __future__ import annotations

import operator
from typing import Annotated, Any, TypedDict, get_args, get_origin, get_type_hints


class MessageState(TypedDict):
    messages: Annotated[list[str], operator.add]
    current_step: str
    sentiment: str


def merge_state(base: MessageState, update: dict[str, Any]) -> MessageState:
    merged = dict(base)
    hints = get_type_hints(MessageState, include_extras=True)
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


def receive_message(state: MessageState) -> dict[str, Any]:
    return {
        'messages': ['Usuario: Necesito ayuda con mi pedido'],
        'current_step': 'received',
    }


def analyze_sentiment(state: MessageState) -> dict[str, Any]:
    latest = state['messages'][-1].lower()
    sentiment = 'negative' if 'ayuda' in latest else 'neutral'
    return {
        'messages': [f'Sistema: sentiment={sentiment}'],
        'current_step': 'analyzed',
        'sentiment': sentiment,
    }


def main() -> None:
    state: MessageState = {
        'messages': [],
        'current_step': 'created',
        'sentiment': 'unknown',
    }
    for node in (receive_message, analyze_sentiment):
        state = merge_state(state, node(state))
    print('Estado final:', state)


if __name__ == '__main__':
    main()
