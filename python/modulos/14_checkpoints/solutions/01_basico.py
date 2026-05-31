from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict


class ReviewState(TypedDict):
    thread_id: str
    step: str
    approved: bool


class FileCheckpoint:
    def __init__(self, path: Path) -> None:
        self.path = path

    def save(self, state: ReviewState) -> None:
        self.path.write_text(json.dumps(state, indent=2), encoding='utf-8')

    def load(self) -> ReviewState:
        return json.loads(self.path.read_text(encoding='utf-8'))


def main() -> None:
    checkpoint_path = Path(__file__).with_name('runtime_solution_file_checkpoint.json')
    store = FileCheckpoint(checkpoint_path)
    state: ReviewState = {'thread_id': 'review-1', 'step': 'waiting_approval', 'approved': False}
    store.save(state)
    print(store.load())
    checkpoint_path.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
