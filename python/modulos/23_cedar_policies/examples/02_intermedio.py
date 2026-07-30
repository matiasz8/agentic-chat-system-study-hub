#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch


@dataclass
class Policy:
    effect: str
    principal: str
    action: str
    resource: str
    conditions: dict[str, str] = field(default_factory=dict)


class MultiPolicyEvaluator:
    def __init__(
        self,
        policies: list[Policy],
        principal_groups: dict[str, list[str]],
        resource_parents: dict[str, str],
    ) -> None:
        self.policies = policies
        self.principal_groups = principal_groups
        self.resource_parents = resource_parents

    def evaluate(self, principal: str, action: str, resource: str, context: dict[str, str]) -> str:
        principal_scope = {principal, *self.principal_groups.get(principal, [])}
        resource_scope = self._resource_scope(resource)
        matched = []
        for policy in self.policies:
            if policy.principal not in principal_scope and policy.principal != "*":
                continue
            if not (policy.action == "*" or fnmatch(action, policy.action)):
                continue
            if policy.resource not in resource_scope and not any(
                fnmatch(candidate, policy.resource) for candidate in resource_scope
            ):
                continue
            if any(context.get(key) != value for key, value in policy.conditions.items()):
                continue
            matched.append(policy)

        if any(policy.effect == "forbid" for policy in matched):
            return "DENY"
        if any(policy.effect == "permit" for policy in matched):
            return "ALLOW"
        return "DENY"

    def _resource_scope(self, resource: str) -> set[str]:
        scope = {resource}
        current = resource
        while current in self.resource_parents:
            current = self.resource_parents[current]
            scope.add(current)
        return scope


def main() -> None:
    evaluator = MultiPolicyEvaluator(
        policies=[
            Policy(
                "permit", "group:analysts", "read", "folder:finance", {"environment": "internal"}
            ),
            Policy("forbid", "group:interns", "read", "folder:finance"),
            Policy("permit", "user:cfo", "edit", "doc:budget"),
        ],
        principal_groups={
            "user:ana": ["group:analysts"],
            "user:tom": ["group:analysts", "group:interns"],
        },
        resource_parents={
            "doc:budget": "folder:finance",
            "doc:q2": "folder:finance",
        },
    )

    requests = [
        ("user:ana", "read", "doc:q2", {"environment": "internal"}),
        ("user:tom", "read", "doc:q2", {"environment": "internal"}),
        ("user:cfo", "edit", "doc:budget", {"environment": "external"}),
    ]

    print("== Grupos, jerarquías y contexto ==")
    for principal, action, resource, context in requests:
        print(
            f"{principal} {action} {resource} {context} -> {evaluator.evaluate(principal, action, resource, context)}"
        )


if __name__ == "__main__":
    main()
