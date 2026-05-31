# ☁️ Despliegue de Aplicaciones Agentic en AWS

## 📚 Descripción

Diseñar un agente inteligente es solo la mitad del problema; la otra mitad es **desplegarlo** de forma segura, observable y económicamente sostenible. Este módulo explica cómo llevar una aplicación como Ask Sage a AWS combinando **Lambda**, **ECS/Fargate**, **Bedrock**, **S3**, **DynamoDB**, **SQS**, monitoreo y pipelines de CI/CD.

El foco no está en memorizar servicios sino en entender qué responsabilidad resuelve cada uno: Lambda para eventos, ECS para procesos persistentes, Bedrock para acceso administrado a LLMs, SQS para desacoplar y CloudWatch/X-Ray para observabilidad.

## 🎯 Objetivos de Aprendizaje

- [x] Identificar servicios de AWS útiles para aplicaciones de IA agentic
- [x] Entender patrones serverless con Lambda y SQS
- [x] Modelar despliegues en contenedores con ECS/Fargate
- [x] Simular infraestructura como código con conceptos tipo CDK
- [x] Diseñar un pipeline CI/CD hacia ECR y ECS
- [x] Incorporar monitoreo con CloudWatch y trazas con X-Ray
- [x] Analizar decisiones de costo como spot, autoscaling y caching

## 📁 Estructura del Módulo

```
42_deployment_aws/
├── README.md
├── examples/
│   ├── 01_basico.py
│   ├── 02_intermedio.py
│   └── 03_avanzado.py
├── exercises/
│   ├── 01.md
│   ├── 02.md
│   └── 03.md
└── solutions/
    ├── 01.py
    ├── 02.py
    └── 03.py
```

## 🧠 Concepto: mapa mental de despliegue en AWS

```
GitHub Actions / CodePipeline
           |
           v
         [ECR]
           |
           v
      +-----------+
      | ECS/App   |<---- Bedrock
      +-----------+
        |    |
        |    +----> DynamoDB / ElastiCache
        |
        +----> S3
        |
        +----> CloudWatch + X-Ray

Eventos asíncronos:
SQS -> Lambda -> tareas de agente / reintentos / DLQ
```

### Patrón general

1. **Build**: el pipeline construye la imagen y la sube a ECR.
2. **Deploy**: ECS/Fargate corre la API o workers persistentes.
3. **Async**: Lambda procesa eventos cortos o mensajes SQS.
4. **LLM**: Bedrock evita operar modelos propios.
5. **Observability**: CloudWatch y X-Ray ayudan a detectar latencia y fallos.

## 🕰️ Historia y contexto

Antes, desplegar IA implicaba administrar VMs, GPUs y scripts frágiles. AWS fue incorporando servicios gestionados que permiten una plataforma más modular. En aplicaciones agentic modernas, ya no todo corre en un único servidor: parte vive en contenedores, otra en funciones efímeras y otra en servicios gestionados de inferencia.

## 🟢 Básico: patrón Lambda handler

```python
def lambda_handler(event, context):
    records = event.get("Records", [])
    return {"processed": len(records), "request_id": context.aws_request_id}
```

## 🟡 Intermedio: despliegue en ECS/Fargate

```python
task_definition = {
    "cpu": 512,
    "memory": 1024,
    "containers": ["ask-sage-api"],
}
print(task_definition)
```

## 🔴 Avanzado: pipeline con blue/green y rollback

```python
deployment_state = "green"
if deployment_state != "healthy":
    print("Rollback hacia blue")
```

## 🧪 Panorama de Ejemplos Prácticos

- **`examples/01_basico.py`**: simulación de Lambda para invocaciones event-driven.
- **`examples/02_intermedio.py`**: manifiesto ECS con health checks, env vars y autoscaling.
- **`examples/03_avanzado.py`**: pipeline con blue/green, monitoreo y rollback.

## 🏋️ Panorama de Ejercicios

- **Ejercicio 1**: handler Lambda que consume SQS y deriva fallos a DLQ.
- **Ejercicio 2**: especificación tipo CDK para VPC, ECS, RDS y ElastiCache.
- **Ejercicio 3**: simulador de pipeline completo desde source hasta rollback.

## ⚖️ Alternativas y comparaciones

| Opción | Ventajas | Desventajas | Cuándo usarla |
|---|---|---|---|
| Lambda + SQS | Escala por evento | Límites de duración | Procesos breves |
| ECS/Fargate | Contenedores sin nodos | Coste mayor que serverless puro | APIs y workers |
| EKS/Kubernetes | Máxima flexibilidad | Complejidad alta | Plataformas grandes |
| Bedrock | LLM administrado | Menos control que self-hosting | Integración rápida |
| EC2 autogestionado | Control total | Más trabajo operativo | Casos especiales |

## 📚 Recursos

- AWS Lambda: https://docs.aws.amazon.com/lambda/
- Amazon ECS: https://docs.aws.amazon.com/ecs/
- AWS Bedrock: https://docs.aws.amazon.com/bedrock/
- AWS CDK: https://docs.aws.amazon.com/cdk/
- AWS Cost Optimization Pillar: https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html
- AWS X-Ray: https://docs.aws.amazon.com/xray/

## 🔗 Próximos pasos

1. Ejecuta los ejemplos para reconocer qué parte de la app vive en Lambda y cuál en ECS.
2. Resuelve el ejercicio de infraestructura antes de tocar CDK real.
3. Diseña un pipeline mental: build, test, push, deploy, smoke test, rollback.
4. Usa este módulo como puente entre diseño de agentes y operación productiva.
