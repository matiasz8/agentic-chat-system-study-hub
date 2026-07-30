from __future__ import annotations

import operator
from collections.abc import Callable
from typing import Annotated, TypedDict


class PipelineState(TypedDict):
    raw_text: str
    steps: Annotated[list[str], operator.add]
    result: str


def collect(state: PipelineState) -> dict[str, object]:
    return {"steps": ["collect"], "result": state["raw_text"].strip()}


def transform(state: PipelineState) -> dict[str, object]:
    return {"steps": ["transform"], "result": state["result"].replace(" ", "_").upper()}


def store(state: PipelineState) -> dict[str, object]:
    return {"steps": ["store"], "result": f"STORED::{state['result']}"}


def apply_edge(
    node: Callable[[PipelineState], dict[str, object]],
    state: PipelineState,
) -> PipelineState:
    update = node(state)
    state["steps"] += update["steps"]  # type: ignore[operator]
    state["result"] = update["result"]  # type: ignore[assignment]
    return state


def main() -> None:
    state: PipelineState = {"raw_text": "resolver incidente", "steps": [], "result": ""}
    for node in (collect, transform, store):
        state = apply_edge(node, state)
    print(state)


if __name__ == "__main__":
    main()
