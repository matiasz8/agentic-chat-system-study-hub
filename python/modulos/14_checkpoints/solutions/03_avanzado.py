from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, TypedDict
from uuid import uuid4
import operator


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
        self.path.write_text(
            json.dumps({'owner': owner, 'state': state}, indent=2),
            encoding='utf-8',
        )

    def resume(self) -> tuple[str, DistributedState]:
        payload = json.loads(self.path.read_text(encoding='utf-8'))
        return payload['owner'], payload['state']


def add_span(state: DistributedState, span: str) -> DistributedState:
    return {
        **state,
        'checkpoint_version': state['checkpoint_version'] + 1,
        'spans': state['spans'] + [span],
    }


def main() -> None:
    checkpoint_path = Path(__file__).with_name('runtime_solution_distributed_checkpoint.json')
    store = DistributedCheckpoint(checkpoint_path)
    state: DistributedState = {
        'thread_id': 'dist-9',
        'trace_id': str(uuid4()),
        'step': 'dispatch',
        'checkpoint_version': 0,
        'spans': [],
    }
    state = add_span(state, 'dispatch.started')
    store.save('worker-primary', state)
    owner, restored = store.resume()
    restored = add_span(restored, 'resume.finished')
    print('Owner:', owner)
    print('State:', restored)
    checkpoint_path.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
