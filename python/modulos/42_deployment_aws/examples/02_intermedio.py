#!/usr/bin/env python3
"""Simulación intermedia de un despliegue ECS/Fargate."""

import json


def build_ecs_manifest() -> dict:
    return {
        "service": "ask-sage-api",
        "task_definition": {
            "cpu": 512,
            "memory": 1024,
            "container_image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/ask-sage:1.0.0",
            "environment": {
                "APP_ENV": "production",
                "BEDROCK_MODEL": "anthropic.claude-3-5-sonnet",
                "CACHE_TTL_SECONDS": "300",
            },
            "health_check": {
                "path": "/health",
                "interval_seconds": 30,
                "timeout_seconds": 5,
            },
        },
        "autoscaling": {
            "min_tasks": 2,
            "max_tasks": 6,
            "target_cpu_percent": 60,
        },
        "cost_optimization": {
            "spot_workers": True,
            "cache_enabled": True,
        },
    }


def main() -> None:
    manifest = build_ecs_manifest()
    print("=== Deployment AWS · Intermedio ===")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    print("\nResumen:")
    print(f"- Servicio: {manifest['service']}")
    print(f"- Health check: {manifest['task_definition']['health_check']['path']}")
    print(f"- Escalado máximo: {manifest['autoscaling']['max_tasks']} tareas")


if __name__ == "__main__":
    main()
