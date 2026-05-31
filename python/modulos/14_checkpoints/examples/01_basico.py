from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict


class CheckpointState(TypedDict):
    thread_id: str
    step: str
    processed_items: int


class FileCheckpoint:
    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, state: CheckpointState) -> None:
        self.path.write_text(json.dumps(state, indent=2), encoding='utf-8')

    def load(self) -> CheckpointState:
        return json.loads(self.path.read_text(encoding='utf-8'))


def main() -> None:
    checkpoint_path = Path(__file__).with_name('runtime_file_checkpoint.json')
    store = FileCheckpoint(checkpoint_path)
    state: CheckpointState = {'thread_id': 'thread-1', 'step': 'extract', 'processed_items': 12}
    store.save(state)
    restored = store.load()
    print('Restored:', restored)
    checkpoint_path.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
