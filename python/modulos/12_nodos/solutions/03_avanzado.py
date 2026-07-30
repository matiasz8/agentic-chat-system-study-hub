from __future__ import annotations

import asyncio
import operator
from collections.abc import Callable
from typing import Annotated, TypedDict


class StreamState(TypedDict):
    text: str
    chunks: Annotated[list[str], operator.add]
    events: Annotated[list[str], operator.add]
    result: str


class StreamingNode:
    def __init__(
        self,
        on_start: Callable[[str], None],
        on_chunk: Callable[[str], None],
        on_finish: Callable[[str], None],
    ) -> None:
        self.on_start = on_start
        self.on_chunk = on_chunk
        self.on_finish = on_finish

    async def invoke(self, state: StreamState) -> dict[str, object]:
        self.on_start(state["text"])
        chunks: list[str] = []
        for word in state["text"].split():
            await asyncio.sleep(0.01)
            token = word[::-1]
            self.on_chunk(token)
            chunks.append(token)
        result = " ".join(chunks)
        self.on_finish(result)
        return {
            "chunks": chunks,
            "events": [f"count={len(chunks)}", "done"],
            "result": result,
        }


async def main() -> None:
    callback_log: list[str] = []
    node = StreamingNode(
        on_start=lambda value: callback_log.append(f"start:{value}"),
        on_chunk=lambda value: callback_log.append(f"chunk:{value}"),
        on_finish=lambda value: callback_log.append(f"finish:{value}"),
    )
    state: StreamState = {
        "text": "callback streaming node",
        "chunks": [],
        "events": [],
        "result": "",
    }
    update = await node.invoke(state)
    state["chunks"] += update["chunks"]  # type: ignore[operator]
    state["events"] += update["events"]  # type: ignore[operator]
    state["result"] = update["result"]  # type: ignore[assignment]
    print("State:", state)
    print("Callback log:", callback_log)


if __name__ == "__main__":
    asyncio.run(main())
