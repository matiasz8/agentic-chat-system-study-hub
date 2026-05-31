from __future__ import annotations

import operator
from typing import Annotated, TypedDict


class TicketNodeState(TypedDict):
    raw_text: str
    processed_steps: Annotated[list[str], operator.add]
    normalized: str


def simple_processor(state: TicketNodeState) -> dict[str, object]:
    normalized = ' '.join(state['raw_text'].strip().lower().split())
    return {'processed_steps': ['simple_processor'], 'normalized': normalized}


def main() -> None:
    state: TicketNodeState = {
        'raw_text': '  INCIDENTE   crítico ',
        'processed_steps': [],
        'normalized': '',
    }
    update = simple_processor(state)
    state['processed_steps'] += update['processed_steps']  # type: ignore[operator]
    state['normalized'] = update['normalized']  # type: ignore[assignment]
    print(state)


if __name__ == '__main__':
    main()
