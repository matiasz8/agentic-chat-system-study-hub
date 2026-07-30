from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated, Any, TypedDict, get_args, get_origin, get_type_hints


def merge_events(
    current: list[dict[str, str]],
    update: list[dict[str, str]],
) -> list[dict[str, str]]:
    return current + update


class AuditState(TypedDict):
    record: dict[str, str]
    audit_log: Annotated[list[dict[str, str]], merge_events]
    current_step: str


@dataclass
class StateObserver:
    actor: str
    on_event: Callable[[dict[str, str]], None]


def merge_state(
    base: AuditState,
    update: dict[str, Any],
    observer: StateObserver,
) -> AuditState:
    merged = dict(base)
    before_snapshot = dict(base["record"])
    hints = get_type_hints(AuditState, include_extras=True)
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
    observer.on_event(
        {
            "actor": observer.actor,
            "timestamp": datetime.now(UTC).isoformat(),
            "before": str(before_snapshot),
            "after": str(merged["record"]),
        }
    )
    return merged  # type: ignore[return-value]


def approve_record(state: AuditState) -> dict[str, Any]:
    updated = dict(state["record"])
    updated["status"] = "approved"
    return {
        "record": updated,
        "audit_log": [
            {
                "change": "status->approved",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        ],
        "current_step": "approved",
    }


def main() -> None:
    observed: list[dict[str, str]] = []
    observer = StateObserver(actor="reviewer-1", on_event=observed.append)
    state: AuditState = {
        "record": {"request_id": "REQ-7", "status": "pending"},
        "audit_log": [],
        "current_step": "created",
    }
    state = merge_state(state, approve_record(state), observer)
    print("State:", state)
    print("Observed events:", observed)


if __name__ == "__main__":
    main()
