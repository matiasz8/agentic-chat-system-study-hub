#!/usr/bin/env python3
"""Solución del ejercicio 3 del módulo Deployment AWS."""

import time
from dataclasses import dataclass


@dataclass
class Stage:
    name: str
    success: bool
    duration_seconds: float


class PipelineSimulator:
    def __init__(self) -> None:
        self.active_color = "blue"

    def stage(self, name: str, success: bool) -> Stage:
        start = time.perf_counter()
        time.sleep(0.01)
        return Stage(name, success, round(time.perf_counter() - start, 4))

    def run(self, smoke_test_success: bool) -> list[Stage]:
        stages = [
            self.stage("source", True),
            self.stage("build", True),
            self.stage("test", True),
            self.stage("push-ecr", True),
            self.stage("deploy-ecs", True),
            self.stage("smoke-test", smoke_test_success),
        ]
        if smoke_test_success:
            self.active_color = "green"
            stages.append(self.stage("traffic-switch", True))
        else:
            stages.append(self.stage("rollback", True))
        return stages


def main() -> None:
    simulator = PipelineSimulator()
    stages = simulator.run(smoke_test_success=False)
    print("=== Solución 3 ===")
    for stage in stages:
        status = "ok" if stage.success else "failed"
        print(f"- {stage.name}: {status} ({stage.duration_seconds}s)")
    print(f"Color activo final: {simulator.active_color}")


if __name__ == "__main__":
    main()
