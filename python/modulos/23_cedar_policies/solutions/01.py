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


class PolicyStore:
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
            return "DENY"
        if any(policy.effect == "permit" for policy in matched):
            return "ALLOW"
        return "DENY"

    @staticmethod
    def _match(pattern: str, value: str) -> bool:
        return pattern == "*" or fnmatch(value, pattern)


def main() -> None:
    store = PolicyStore(
        [
            Policy("permit", "user:ana", "read", "doc:*"),
            Policy("forbid", "user:ana", "delete", "doc:*"),
            Policy("permit", "user:admin", "*", "*"),
        ]
    )
    for case in [
        ("user:ana", "read", "doc:q1"),
        ("user:ana", "delete", "doc:q1"),
        ("user:luis", "read", "doc:q1"),
    ]:
        print(case, "->", store.evaluate(*case))


if __name__ == "__main__":
    main()
