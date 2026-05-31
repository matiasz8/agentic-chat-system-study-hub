#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from ipaddress import ip_address, ip_network
from typing import Dict, List


@dataclass
class Policy:
    policy_id: str
    effect: str
    principal: str
    action: str
    resource: str
    conditions: Dict[str, object]


class AuthorizationService:
    def __init__(self, policies: List[Policy], groups: Dict[str, List[str]], parents: Dict[str, str]) -> None:
        self.policies = policies
        self.groups = groups
        self.parents = parents
        self.audit: List[str] = []

    def evaluate(self, principal: str, action: str, resource: str, context: Dict[str, str]) -> str:
        principal_scope = {principal, *self.groups.get(principal, [])}
        resource_scope = {resource}
        current = resource
        while current in self.parents:
            current = self.parents[current]
            resource_scope.add(current)

        matched = []
        for policy in self.policies:
            if policy.principal not in principal_scope:
                continue
            if policy.action != action:
                continue
            if policy.resource not in resource_scope:
                continue
            if not self._check_conditions(policy.conditions, context):
                continue
            matched.append(policy)

        if any(policy.effect == "forbid" for policy in matched):
            decision = "DENY"
        elif any(policy.effect == "permit" for policy in matched):
            decision = "ALLOW"
        else:
            decision = "DENY"

        self.audit.append(f"{principal}:{action}:{resource} -> {decision} ({[p.policy_id for p in matched]})")
        return decision

    def _check_conditions(self, conditions: Dict[str, object], context: Dict[str, str]) -> bool:
        if "tenant" in conditions and context.get("tenant") != conditions["tenant"]:
            return False
        if "ip_in" in conditions:
            current_ip = ip_address(context["ip"])
            if not any(current_ip in ip_network(net) for net in conditions["ip_in"]):
                return False
        if "time_between" in conditions:
            start, end = conditions["time_between"]
            current = datetime.strptime(context["time"], "%H:%M").time()
            if not (datetime.strptime(start, "%H:%M").time() <= current <= datetime.strptime(end, "%H:%M").time()):
                return False
        return True


def main() -> None:
    service = AuthorizationService(
        policies=[
            Policy("p1", "permit", "group:analysts", "read", "folder:finance", {"tenant": "acme", "ip_in": ["10.0.0.0/24"], "time_between": ["08:00", "18:00"]}),
            Policy("p2", "forbid", "group:contractors", "read", "folder:finance", {}),
        ],
        groups={"user:ana": ["group:analysts"], "user:bob": ["group:analysts", "group:contractors"]},
        parents={"doc:q2": "folder:finance"},
    )

    print(service.evaluate("user:ana", "read", "doc:q2", {"tenant": "acme", "ip": "10.0.0.3", "time": "09:00"}))
    print(service.evaluate("user:bob", "read", "doc:q2", {"tenant": "acme", "ip": "10.0.0.4", "time": "09:00"}))
    print("\n".join(service.audit))


if __name__ == "__main__":
    main()
