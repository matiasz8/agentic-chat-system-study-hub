from __future__ import annotations

from typing import Literal, TypedDict


class RouteState(TypedDict):
    payload: str
    score: int
    next_node: str
    outcome: str


def validation_router(state: RouteState) -> Literal['process', 'manual_review', 'reject']:
    if not state['payload'].strip():
        return 'reject'
    if state['score'] < 50:
        return 'manual_review'
    return 'process'


def process_node(state: RouteState) -> dict[str, str]:
    return {'next_node': 'done', 'outcome': 'processed'}


def manual_review_node(state: RouteState) -> dict[str, str]:
    return {'next_node': 'done', 'outcome': 'manual_review'}


def reject_node(state: RouteState) -> dict[str, str]:
    return {'next_node': 'done', 'outcome': 'rejected'}


def main() -> None:
    handlers = {
        'process': process_node,
        'manual_review': manual_review_node,
        'reject': reject_node,
    }
    for payload, score in [('lead bueno', 90), ('lead dudoso', 35), ('   ', 0)]:
        state: RouteState = {
            'payload': payload,
            'score': score,
            'next_node': 'router',
            'outcome': '',
        }
        route = validation_router(state)
        state.update(handlers[route](state))
        print(state)


if __name__ == '__main__':
    main()
