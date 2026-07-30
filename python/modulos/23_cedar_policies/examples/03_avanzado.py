#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from fnmatch import fnmatch
from ipaddress import ip_address, ip_network


@dataclass
class Policy:
    policy_id: str
    effect: str
    principal: str
    action: str
    resource: str
    conditions: dict[str, object] = field(default_factory=dict)


@dataclass
class Decision:
    principal: str
    action: str
    resource: str
    allow: bool
    matched_policies: list[str]
    reason: str


class EntityGraph:
    def __init__(self) -> None:
        self.principal_parents: dict[str, list[str]] = {}
        self.resource_parents: dict[str, str] = {}

    def add_principal_parent(self, principal: str, parent: str) -> None:
        self.principal_parents.setdefault(principal, []).append(parent)

    def add_resource_parent(self, resource: str, parent: str) -> None:
        self.resource_parents[resource] = parent

    def principal_scope(self, principal: str) -> set[str]:
        scope = {principal}
        pending = [principal]
        while pending:
            current = pending.pop()
            for parent in self.principal_parents.get(current, []):
                if parent not in scope:
                    scope.add(parent)
                    pending.append(parent)
        return scope

    def resource_scope(self, resource: str) -> set[str]:
        scope = {resource}
        current = resource
        while current in self.resource_parents:
            current = self.resource_parents[current]
            scope.add(current)
        return scope


class AuthorizationService:
    def __init__(self, policies: list[Policy], entity_graph: EntityGraph) -> None:
        self.policies = policies
        self.entity_graph = entity_graph
        self.audit_log: list[Decision] = []

    def evaluate(
        self, principal: str, action: str, resource: str, context: dict[str, str]
    ) -> Decision:
        principal_scope = self.entity_graph.principal_scope(principal)
        resource_scope = self.entity_graph.resource_scope(resource)
        matched: list[Policy] = []

        for policy in self.policies:
            if policy.principal != "*" and policy.principal not in principal_scope:
                continue
            if not (policy.action == "*" or fnmatch(action, policy.action)):
                continue
            if (
                policy.resource != "*"
                and policy.resource not in resource_scope
                and not any(fnmatch(candidate, policy.resource) for candidate in resource_scope)
            ):
                continue
            if not self._check_conditions(policy.conditions, context):
                continue
            matched.append(policy)

        if any(policy.effect == "forbid" for policy in matched):
            decision = Decision(
                principal,
                action,
                resource,
                False,
                [p.policy_id for p in matched],
                "forbid explícito",
            )
        elif any(policy.effect == "permit" for policy in matched):
            decision = Decision(
                principal,
                action,
                resource,
                True,
                [p.policy_id for p in matched],
                "permit encontrado",
            )
        else:
            decision = Decision(principal, action, resource, False, [], "default deny")

        self.audit_log.append(decision)
        return decision

    def _check_conditions(self, conditions: dict[str, object], context: dict[str, str]) -> bool:
        equals = conditions.get("equals", {})
        if isinstance(equals, dict):
            for key, expected in equals.items():
                if context.get(key) != expected:
                    return False

        ip_ranges = conditions.get("ip_in")
        if ip_ranges:
            current_ip = ip_address(context["ip"])
            if not any(current_ip in ip_network(net) for net in ip_ranges):
                return False

        time_between = conditions.get("time_between")
        if time_between:
            start, end = time_between
            current = datetime.strptime(context["time"], "%H:%M").time()
            if not (
                datetime.strptime(start, "%H:%M").time()
                <= current
                <= datetime.strptime(end, "%H:%M").time()
            ):
                return False

        return True


def main() -> None:
    graph = EntityGraph()
    graph.add_principal_parent("user:ana", "group:analysts")
    graph.add_principal_parent("user:bob", "group:analysts")
    graph.add_principal_parent("user:bob", "group:contractors")
    graph.add_principal_parent("user:carla", "group:admins")
    graph.add_resource_parent("doc:q2", "folder:finance")
    graph.add_resource_parent("folder:finance", "tenant:acme")

    service = AuthorizationService(
        policies=[
            Policy(
                "permit-finance-read",
                "permit",
                "group:analysts",
                "read",
                "folder:finance",
                {
                    "equals": {"tenant": "acme"},
                    "ip_in": ["10.0.0.0/24"],
                    "time_between": ["08:00", "18:00"],
                },
            ),
            Policy("forbid-contractors", "forbid", "group:contractors", "read", "folder:finance"),
            Policy("permit-admin-delete", "permit", "group:admins", "delete", "*"),
        ],
        entity_graph=graph,
    )

    requests = [
        ("user:ana", "read", "doc:q2", {"tenant": "acme", "ip": "10.0.0.25", "time": "10:30"}),
        ("user:bob", "read", "doc:q2", {"tenant": "acme", "ip": "10.0.0.30", "time": "11:00"}),
        ("user:carla", "delete", "doc:q2", {"tenant": "acme", "ip": "10.0.0.40", "time": "09:00"}),
    ]

    print("== Servicio de autorización Cedar-inspired ==")
    for request in requests:
        decision = service.evaluate(*request)
        print(json.dumps(asdict(decision), ensure_ascii=False))


if __name__ == "__main__":
    main()
