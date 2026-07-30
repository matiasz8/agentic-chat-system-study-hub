#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Policy:
    effect: str
    principal: str
    action: str
    resource: str


class GroupPolicyStore:
    def __init__(
        self, policies: list[Policy], groups: dict[str, list[str]], parents: dict[str, str]
    ) -> None:
        self.policies = policies
        self.groups = groups
        self.parents = parents

    def evaluate(self, principal: str, action: str, resource: str) -> str:
        principal_scope = {principal, *self.groups.get(principal, [])}
        resource_scope = {resource}
        current = resource
        while current in self.parents:
            current = self.parents[current]
            resource_scope.add(current)

        matched = [
            policy
            for policy in self.policies
            if policy.principal in principal_scope
            and policy.action == action
            and policy.resource in resource_scope
        ]
        if any(policy.effect == "forbid" for policy in matched):
            return "DENY"
        if any(policy.effect == "permit" for policy in matched):
            return "ALLOW"
        return "DENY"


def main() -> None:
    store = GroupPolicyStore(
        policies=[
            Policy("permit", "group:analysts", "read", "folder:finance"),
            Policy("forbid", "group:interns", "read", "folder:finance"),
        ],
        groups={"user:ana": ["group:analysts"], "user:tom": ["group:analysts", "group:interns"]},
        parents={"doc:q2": "folder:finance"},
    )
    print(store.evaluate("user:ana", "read", "doc:q2"))
    print(store.evaluate("user:tom", "read", "doc:q2"))


if __name__ == "__main__":
    main()
