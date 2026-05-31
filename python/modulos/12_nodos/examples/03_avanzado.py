from __future__ import annotations

import asyncio
from collections.abc import Callable
import operator
from typing import Annotated, TypedDict


class StreamState(TypedDict):
    incoming_text: str
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
        self.on_start(state['incoming_text'])
        chunks: list[str] = []
        for word in state['incoming_text'].split():
            await asyncio.sleep(0.02)
            token = word.upper()
            self.on_chunk(token)
            chunks.append(token)
        result = ' | '.join(chunks)
        self.on_finish(result)
        return {
            'chunks': chunks,
            'events': [f'chunks={len(chunks)}', 'stream_completed'],
            'result': result,
        }


async def main() -> None:
    events: list[str] = []
    node = StreamingNode(
        on_start=lambda text: events.append(f'start:{text}'),
        on_chunk=lambda chunk: events.append(f'chunk:{chunk}'),
        on_finish=lambda result: events.append(f'finish:{result}'),
    )
    state: StreamState = {
        'incoming_text': 'streaming response ready',
        'chunks': [],
        'events': [],
        'result': '',
    }
    update = await node.invoke(state)
    state['chunks'] += update['chunks']  # type: ignore[operator]
    state['events'] += update['events']  # type: ignore[operator]
    state['result'] = update['result']  # type: ignore[assignment]
    print('State:', state)
    print('Callbacks:', events)


if __name__ == '__main__':
    asyncio.run(main())
