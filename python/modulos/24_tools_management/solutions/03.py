#!/usr/bin/env python3
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from dataclasses import dataclass
from typing import Any, Callable, List
import time


class TransientToolError(RuntimeError):
    pass


@dataclass
class LogEntry:
    tool_name: str
    attempt: int
    status: str
    detail: str


@dataclass
class Tool:
    name: str
    timeout_seconds: float
    func: Callable[..., Any]


class ToolExecutor:
    def __init__(self, retries: int = 2) -> None:
        self.retries = retries
        self.logs: List[LogEntry] = []

    def invoke(self, tool: Tool, **payload: Any) -> Any:
        for attempt in range(1, self.retries + 2):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(tool.func, **payload)
                try:
                    result = future.result(timeout=tool.timeout_seconds)
                    self.logs.append(LogEntry(tool.name, attempt, "ok", repr(result)))
                    return result
                except FuturesTimeoutError:
                    self.logs.append(LogEntry(tool.name, attempt, "timeout", "timeout excedido"))
                    return {"status": "timeout"}
                except TransientToolError as exc:
                    self.logs.append(LogEntry(tool.name, attempt, "retry", str(exc)))
                    if attempt > self.retries:
                        return {"status": "error", "detail": str(exc)}
                except Exception as exc:
                    self.logs.append(LogEntry(tool.name, attempt, "error", str(exc)))
                    return {"status": "error", "detail": str(exc)}
        return {"status": "error", "detail": "sin resultado"}


class FlakyTool:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, query: str) -> str:
        self.calls += 1
        if self.calls == 1:
            raise TransientToolError(f"fallo transitorio para {query}")
        return f"recuperado para {query}"


def slow_tool(query: str) -> str:
    time.sleep(0.2)
    return query


def main() -> None:
    executor = ToolExecutor(retries=2)
    flaky = Tool("flaky_search", 1.0, FlakyTool())
    slow = Tool("slow_search", 0.05, slow_tool)

    print(executor.invoke(flaky, query="cedar"))
    print(executor.invoke(slow, query="agentcore"))

    print("\n== Logs ==")
    for log in executor.logs:
        print(log)


if __name__ == "__main__":
    main()
