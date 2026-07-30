from __future__ import annotations

import json
import operator
from pathlib import Path
from typing import Annotated, TypedDict
from uuid import uuid4


class DistributedState(TypedDict):
    thread_id: str
    trace_id: str
    step: str
    checkpoint_version: int
    spans: Annotated[list[str], operator.add]


class DistributedCheckpoint:
    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, owner: str, state: DistributedState) -> None:
        payload = {"owner": owner, "state": state}
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def resume(self) -> tuple[str, DistributedState]:
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return payload["owner"], payload["state"]


def append_span(state: DistributedState, span_name: str) -> DistributedState:
    return {
        **state,
        "checkpoint_version": state["checkpoint_version"] + 1,
        "spans": state["spans"] + [span_name],
    }


def main() -> None:
    checkpoint_path = Path(__file__).with_name("runtime_distributed_checkpoint.json")
    store = DistributedCheckpoint(checkpoint_path)
    state: DistributedState = {
        "thread_id": "thread-distributed",
        "trace_id": str(uuid4()),
        "step": "dispatch",
        "checkpoint_version": 0,
        "spans": [],
    }
    state = append_span(state, "dispatch.started")
    store.save("worker-a", state)
    owner, restored = store.resume()
    restored = append_span(restored, "resume.completed")
    print("Owner:", owner)
    print("Restored:", restored)
    checkpoint_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
