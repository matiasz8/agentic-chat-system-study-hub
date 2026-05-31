from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
import operator
from typing import Annotated, TypedDict


@dataclass
class Worker:
    name: str
    load: int
    should_fail: bool = False

    def handle(self, task: str) -> str:
        if self.should_fail:
            raise RuntimeError(f'worker {self.name} unavailable')
        return f'{self.name}:{task.upper()}'


class RoutingState(TypedDict):
    task: str
    results: Annotated[list[str], operator.add]
    route_log: Annotated[list[str], operator.add]
    fallback_used: bool


def choose_targets(workers: list[Worker], parallelism: int) -> list[Worker]:
    return sorted(workers, key=lambda worker: worker.load)[:parallelism]


def run_with_fallback(state: RoutingState, workers: list[Worker], fallback: Worker) -> RoutingState:
    selected = choose_targets(workers, parallelism=2)
    state['route_log'] += [f'selected:{worker.name}' for worker in selected]
    with ThreadPoolExecutor(max_workers=len(selected)) as executor:
        futures = [executor.submit(worker.handle, state['task']) for worker in selected]
        for future in futures:
            try:
                state['results'].append(future.result())
            except RuntimeError as exc:
                state['fallback_used'] = True
                state['route_log'].append(f'fallback:{exc}')
                state['results'].append(fallback.handle(state['task']))
    return state


def main() -> None:
    workers = [Worker('w1', load=1), Worker('w2', load=2, should_fail=True), Worker('w3', load=4)]
    fallback = Worker('backup', load=0)
    state: RoutingState = {'task': 'classify lead', 'results': [], 'route_log': [], 'fallback_used': False}
    final_state = run_with_fallback(state, workers, fallback)
    print(final_state)


if __name__ == '__main__':
    main()
