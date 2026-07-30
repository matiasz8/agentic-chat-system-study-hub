from __future__ import annotations

from typing import Literal, TypedDict


class RouteState(TypedDict):
    payload: str
    score: int
    next_node: str
    outcome: str


def validation_router(state: RouteState) -> Literal["process", "reject", "manual_review"]:
    if not state["payload"].strip():
        return "reject"
    if state["score"] < 50:
        return "manual_review"
    return "process"


def process_node(state: RouteState) -> dict[str, str]:
    return {"next_node": "done", "outcome": "processed"}


def reject_node(state: RouteState) -> dict[str, str]:
    return {"next_node": "done", "outcome": "rejected"}


def manual_review_node(state: RouteState) -> dict[str, str]:
    return {"next_node": "done", "outcome": "manual_review"}


def run_case(payload: str, score: int) -> None:
    state: RouteState = {"payload": payload, "score": score, "next_node": "router", "outcome": ""}
    route = validation_router(state)
    handlers = {
        "process": process_node,
        "reject": reject_node,
        "manual_review": manual_review_node,
    }
    state.update(handlers[route](state))
    print(state)


def main() -> None:
    run_case("mensaje válido", 91)
    run_case("mensaje sospechoso", 10)
    run_case("   ", 0)


if __name__ == "__main__":
    main()
