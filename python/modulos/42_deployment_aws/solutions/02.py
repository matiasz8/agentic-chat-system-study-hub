#!/usr/bin/env python3
"""Solución del ejercicio 2 del módulo Deployment AWS."""

from dataclasses import asdict, dataclass, field
import json


@dataclass
class VPC:
    cidr: str
    public_subnets: int
    private_subnets: int


@dataclass
class ECSService:
    name: str
    cpu: int
    memory: int
    desired_count: int


@dataclass
class RDSInstance:
    engine: str
    instance_class: str
    multi_az: bool


@dataclass
class ElastiCacheCluster:
    engine: str
    node_type: str
    replicas: int


@dataclass
class StackSpec:
    environment: str
    vpc: VPC
    ecs: ECSService
    rds: RDSInstance
    cache: ElastiCacheCluster
    tags: dict[str, str] = field(default_factory=dict)


def main() -> None:
    stack = StackSpec(
        environment="prod",
        vpc=VPC("10.0.0.0/16", 2, 4),
        ecs=ECSService("ask-sage-api", 1024, 2048, 3),
        rds=RDSInstance("postgres", "db.t4g.medium", True),
        cache=ElastiCacheCluster("redis", "cache.t4g.small", 2),
        tags={"owner": "nanlabs", "system": "ask-sage"},
    )
    print("=== Solución 2 ===")
    print(json.dumps(asdict(stack), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
