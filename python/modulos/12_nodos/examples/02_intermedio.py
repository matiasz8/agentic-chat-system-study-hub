from __future__ import annotations

import asyncio
import operator
from typing import Annotated, TypedDict


class ErrorState(TypedDict):
    payload: str
    retries: int
    errors: Annotated[list[str], operator.add]
    result: str


async def fetch_and_transform(payload: str) -> str:
    await asyncio.sleep(0.05)
    if not payload.strip():
        raise ValueError("payload vacío")
    return payload.upper()


async def error_handling_node(state: ErrorState) -> dict[str, object]:
    try:
        transformed = await fetch_and_transform(state["payload"])
        return {"result": transformed}
    except Exception as exc:
        return {
            "retries": state["retries"] + 1,
            "errors": [f"{exc.__class__.__name__}: {exc}"],
            "result": "FALLBACK",
        }


async def run_case(payload: str) -> None:
    state: ErrorState = {"payload": payload, "retries": 0, "errors": [], "result": ""}
    update = await error_handling_node(state)
    state["retries"] = update.get("retries", state["retries"])  # type: ignore[arg-type]
    state["errors"] += update.get("errors", [])  # type: ignore[arg-type]
    state["result"] = update["result"]  # type: ignore[assignment]
    print(state)


async def main() -> None:
    await run_case("ticket aprobado")
    await run_case("   ")


if __name__ == "__main__":
    asyncio.run(main())
