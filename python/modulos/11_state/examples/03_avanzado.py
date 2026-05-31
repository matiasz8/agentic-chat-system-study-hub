from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Any, TypedDict, get_args, get_origin, get_type_hints


def merge_audit(
    current: list[dict[str, str]],
    update: list[dict[str, str]],
) -> list[dict[str, str]]:
    return current + update


class AuditState(TypedDict):
    values: dict[str, str]
    audit_log: Annotated[list[dict[str, str]], merge_audit]
    current_step: str


@dataclass
class StateObserver:
    on_update: Callable[[dict[str, str]], None]


def merge_state(
    base: AuditState,
    update: dict[str, Any],
    observer: StateObserver,
) -> AuditState:
    merged = dict(base)
    hints = get_type_hints(AuditState, include_extras=True)
    before_snapshot = dict(base['values'])
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
    observer.on_update(
        {
            'step': merged['current_step'],
            'before': str(before_snapshot),
            'after': str(merged['values']),
        }
    )
    return merged  # type: ignore[return-value]


def enrich_customer(state: AuditState) -> dict[str, Any]:
    new_values = dict(state['values'])
    new_values['segment'] = 'vip' if state['values']['spend'] == 'high' else 'standard'
    return {
        'values': new_values,
        'audit_log': [
            {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'change': 'segment calculated',
            }
        ],
        'current_step': 'enriched',
    }


def main() -> None:
    events: list[dict[str, str]] = []
    observer = StateObserver(on_update=events.append)
    state: AuditState = {
        'values': {'customer_id': 'C-1', 'spend': 'high'},
        'audit_log': [],
        'current_step': 'created',
    }
    state = merge_state(state, enrich_customer(state), observer)
    print('State final:', state)
    print('Eventos observados:', events)


if __name__ == '__main__':
    main()
