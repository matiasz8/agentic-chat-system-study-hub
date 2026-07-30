from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

try:
    import sqlite3
except ModuleNotFoundError:
    sqlite3 = None


class CheckpointState(TypedDict):
    thread_id: str
    step: str
    version: int
    payload: dict[str, str]


class DBCheckpoint:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.mode = "sqlite" if sqlite3 is not None else "json"
        if self.mode == "sqlite":
            self.connection = sqlite3.connect(db_path)
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS checkpoints (
                    thread_id TEXT,
                    version INTEGER,
                    step TEXT,
                    payload TEXT,
                    PRIMARY KEY (thread_id, version)
                )
                """
            )
            self.connection.commit()
        else:
            self.connection = None
            if not self.db_path.exists():
                self.db_path.write_text("[]", encoding="utf-8")

    def save(self, state: CheckpointState) -> None:
        if self.mode == "sqlite":
            assert self.connection is not None
            self.connection.execute(
                "INSERT OR REPLACE INTO checkpoints VALUES (?, ?, ?, ?)",
                (
                    state["thread_id"],
                    state["version"],
                    state["step"],
                    json.dumps(state["payload"], sort_keys=True),
                ),
            )
            self.connection.commit()
            return
        rows = json.loads(self.db_path.read_text(encoding="utf-8"))
        rows = [
            row
            for row in rows
            if not (row["thread_id"] == state["thread_id"] and row["version"] == state["version"])
        ]
        rows.append(state)
        rows.sort(key=lambda row: (row["thread_id"], row["version"]))
        self.db_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    def load_latest(self, thread_id: str) -> CheckpointState:
        if self.mode == "sqlite":
            assert self.connection is not None
            row = self.connection.execute(
                """
                SELECT thread_id, step, version, payload
                FROM checkpoints
                WHERE thread_id = ?
                ORDER BY version DESC
                LIMIT 1
                """,
                (thread_id,),
            ).fetchone()
            if row is None:
                raise LookupError(f"Checkpoint not found for {thread_id}")
            return {
                "thread_id": row[0],
                "step": row[1],
                "version": row[2],
                "payload": json.loads(row[3]),
            }
        rows = json.loads(self.db_path.read_text(encoding="utf-8"))
        matches = [row for row in rows if row["thread_id"] == thread_id]
        if not matches:
            raise LookupError(f"Checkpoint not found for {thread_id}")
        return max(matches, key=lambda row: row["version"])

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()


def main() -> None:
    suffix = ".sqlite3" if sqlite3 is not None else ".json"
    db_path = Path(__file__).with_name(f"runtime_solution_checkpoints{suffix}")
    store = DBCheckpoint(db_path)
    try:
        store.save(
            {
                "thread_id": "approval-7",
                "step": "collect",
                "version": 1,
                "payload": {"status": "received"},
            }
        )
        store.save(
            {
                "thread_id": "approval-7",
                "step": "approved",
                "version": 2,
                "payload": {"status": "approved"},
            }
        )
        print("Backend:", store.mode)
        print(store.load_latest("approval-7"))
    finally:
        store.close()
        db_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
