from __future__ import annotations

import operator
from typing import Annotated, Callable, TypedDict


class PipelineState(TypedDict):
    raw_text: str
    steps: Annotated[list[str], operator.add]
    result: str


def collect(state: PipelineState) -> dict[str, object]:
    return {'steps': ['collect'], 'result': state['raw_text'].strip()}


def uppercase(state: PipelineState) -> dict[str, object]:
    return {'steps': ['uppercase'], 'result': state['result'].upper()}


def store(state: PipelineState) -> dict[str, object]:
    return {'steps': ['store'], 'result': f'STORED::{state["result"]}'}


def apply_edge(
    node: Callable[[PipelineState], dict[str, object]],
    state: PipelineState,
) -> PipelineState:
    update = node(state)
    state['steps'] += update['steps']  # type: ignore[operator]
    state['result'] = update['result']  # type: ignore[assignment]
    return state


def main() -> None:
    state: PipelineState = {'raw_text': ' cerrar ticket ', 'steps': [], 'result': ''}
    for node in (collect, uppercase, store):
        state = apply_edge(node, state)
    print(state)


if __name__ == '__main__':
    main()
