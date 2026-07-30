from __future__ import annotations

import asyncio
import operator
from typing import Annotated, TypedDict


class NodeState(TypedDict):
    payload: str
    retries: int
    errors: Annotated[list[str], operator.add]
    result: str


async def fake_external_call(payload: str) -> str:
    await asyncio.sleep(0.05)
    if not payload.strip():
        raise ValueError("payload vacío")
    return f"processed:{payload.lower()}"


async def error_handling_node(state: NodeState) -> dict[str, object]:
    try:
        return {"result": await fake_external_call(state["payload"])}
    except Exception as exc:
        return {
            "retries": state["retries"] + 1,
            "errors": [str(exc)],
            "result": "fallback:manual-review",
        }


async def main() -> None:
    for payload in ("Mensaje válido", "   "):
        state: NodeState = {"payload": payload, "retries": 0, "errors": [], "result": ""}
        update = await error_handling_node(state)
        state["retries"] = update.get("retries", state["retries"])  # type: ignore[arg-type]
        state["errors"] += update.get("errors", [])  # type: ignore[arg-type]
        state["result"] = update["result"]  # type: ignore[assignment]
        print(state)


if __name__ == "__main__":
    asyncio.run(main())
