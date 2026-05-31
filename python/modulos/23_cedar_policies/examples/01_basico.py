#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from typing import List


@dataclass
class Policy:
    effect: str
    principal: str
    action: str
    resource: str


class CedarLikeEvaluator:
    def __init__(self, policies: List[Policy]) -> None:
        self.policies = policies

    def evaluate(self, principal: str, action: str, resource: str) -> str:
        matched = [
            policy
            for policy in self.policies
            if self._match(policy.principal, principal)
            and self._match(policy.action, action)
            and self._match(policy.resource, resource)
        ]
        if any(policy.effect == "forbid" for policy in matched):
            return "DENY (forbid explícito)"
        if any(policy.effect == "permit" for policy in matched):
            return "ALLOW"
        return "DENY (default deny)"

    @staticmethod
    def _match(pattern: str, value: str) -> bool:
        return pattern == "*" or fnmatch(value, pattern)


def main() -> None:
    evaluator = CedarLikeEvaluator(
        policies=[
            Policy("permit", "user:ana", "read", "doc:*"),
            Policy("forbid", "user:ana", "delete", "doc:*"),
            Policy("permit", "user:admin", "*", "*"),
        ]
    )

    requests = [
        ("user:ana", "read", "doc:manual"),
        ("user:ana", "delete", "doc:manual"),
        ("user:luis", "read", "doc:manual"),
        ("user:admin", "archive", "folder:finance"),
    ]

    print("== Evaluación Cedar-like ==")
    for principal, action, resource in requests:
        decision = evaluator.evaluate(principal, action, resource)
        print(f"{principal} {action} {resource} -> {decision}")


if __name__ == "__main__":
    main()
