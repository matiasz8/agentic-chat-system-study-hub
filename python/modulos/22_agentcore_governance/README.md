# 🛡️ Gobernanza de Agentes con AWS AgentCore

## 📚 Descripción

La gobernanza de agentes consiste en poner reglas, observabilidad y límites operativos alrededor de sistemas autónomos. En el ecosistema de **AWS AgentCore**, esto significa definir qué agentes existen, qué herramientas pueden usar, qué huellas dejan en auditoría y cuándo una acción debe ser frenada antes de convertirse en un riesgo de seguridad, costo o cumplimiento.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- [ ] Explicar qué problema resuelve AWS AgentCore en entornos empresariales.
- [ ] Modelar un registro de agentes con capacidades, owner y estado operativo.
- [ ] Diseñar controles de acceso para limitar qué herramientas puede invocar cada agente.
- [ ] Implementar auditoría estructurada para invocaciones de herramientas.
- [ ] Aplicar rate limiting por agente para evitar abuso o loops descontrolados.
- [ ] Entender fronteras de confianza en arquitecturas multiagente.

## 📋 Estructura del Módulo

```text
22_agentcore_governance/
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

## 🧠 Concepto Central

Piensa en AgentCore como la capa donde un agente deja de ser “solo un prompt con herramientas” y pasa a ser un **activo gobernado** dentro de una plataforma.

```text
Usuario / Sistema
       |
       v
+--------------------+
| Agent Registry     |  -> ¿Quién es este agente?
+--------------------+
       |
       v
+--------------------+
| Policy Enforcement |  -> ¿Puede usar esta tool?
+--------------------+
       |
       v
+--------------------+
| Rate Limiter       |  -> ¿Está excediendo su cuota?
+--------------------+
       |
       v
+--------------------+
| Tool Invocation    |  -> Ejecuta acción aprobada
+--------------------+
       |
       v
+--------------------+
| Audit / Tracing    |  -> Guarda inputs, outputs y decisión
+--------------------+
```

### ¿Qué controles suelen aparecer?

1. **Access control**: solo ciertos agentes pueden llamar ciertas tools.
2. **Audit logging**: cada invocación queda registrada con contexto y resultado.
3. **Rate limiting**: evita loops, abuso o costos inesperados.
4. **Trust boundaries**: un agente no debe heredar permisos de otro sin validación explícita.

## 🕰️ Historia y Contexto

Las primeras apps con LLM tendían a conectar modelos con herramientas de forma directa: “si el modelo pide una acción, se ejecuta”. Ese enfoque funciona en demos, pero falla rápido en empresas donde importan la trazabilidad, la separación de funciones y el cumplimiento.

AWS empuja esta conversación con **Amazon Bedrock**, **AgentCore** y servicios adyacentes como **CloudTrail**, **CloudWatch** y **Verified Permissions**. La idea no es solo desplegar agentes, sino tratarlos como componentes auditables y gobernables: igual que una API, una cola o un microservicio crítico.

## 🟢 Nivel Básico: Registro de Agentes

Primero necesitas saber qué agentes existen y qué dicen poder hacer.

```python
registry.register(
    agent_id="finance-bot",
    name="Finance Bot",
    capabilities=["read_reports", "summarize"],
    owner="equipo-finanzas",
)

print(registry.capabilities_of("finance-bot"))
```

**Idea clave**: si no existe un registro central, tampoco existe una base confiable para gobernar.

## 🟡 Nivel Intermedio: Auditoría de Tools

Una vez que el agente ejecuta acciones, necesitas evidencia estructurada.

```python
result = audit_logger.invoke(
    agent_id="support-bot",
    tool_name="search_kb",
    tool_func=search_kb,
    query="politica de devoluciones",
)
```

**Idea clave**: no alcanza con logs de texto; conviene capturar `timestamp`, `agent_id`, `tool_name`, `inputs`, `outputs` y `success`.

## 🔴 Nivel Avanzado: Motor de Gobernanza

La gobernanza real combina políticas, cuotas y alertas.

```python
allowed = engine.invoke(
    agent_id="ops-bot",
    tool_name="restart_service",
    service="billing-api",
)
```

Antes de ejecutar, el motor puede responder preguntas como:

- ¿Ese agente tiene permiso?
- ¿Ya superó el límite de llamadas por minuto?
- ¿Debo generar una alerta por múltiples denegaciones?

## 💼 Panorama de Ejemplos Prácticos

- **`examples/01_basico.py`**: simula un registro de agentes y consulta capacidades.
- **`examples/02_intermedio.py`**: envuelve llamadas a tools con auditoría estructurada.
- **`examples/03_avanzado.py`**: implementa políticas por agente, rate limiting y alertas.

## 🧪 Panorama de Ejercicios

- **Ejercicio 1**: construir un `AgentRegistry` con metadata operativa.
- **Ejercicio 2**: crear un `AuditLogger` que capture invocaciones de tools.
- **Ejercicio 3**: implementar un `GovernanceEngine` con límites y reglas.

## 🔀 Alternativas y Comparación

| Opción | Fortalezas | Debilidades | Cuándo usarla |
|---|---|---|---|
| **AWS AgentCore + observabilidad AWS** | Integración con ecosistema AWS, trazabilidad empresarial | Dependencia de plataforma | Organizaciones ya centradas en AWS |
| **Middleware custom en Python** | Máxima flexibilidad | Más mantenimiento y riesgo de drift | Prototipos o plataformas internas chicas |
| **OPA / Rego** | Políticas muy expresivas y desacopladas | Curva de aprendizaje | Equipos con fuerte cultura policy-as-code |
| **API Gateway + authorizers** | Control fuerte en borde de red | Menos contexto semántico del agente | Herramientas expuestas como APIs |
| **Sin capa de gobernanza** | Velocidad inicial | Alto riesgo operativo | Solo demos o laboratorios efímeros |

## 📚 Recursos

- AWS Bedrock AgentCore: https://aws.amazon.com/bedrock/agentcore/
- Amazon Bedrock Agents: https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
- AWS CloudTrail User Guide: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html
- Amazon CloudWatch Logs: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html
- Amazon Verified Permissions: https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html

## ⏭️ Próximos Pasos

1. Ejecuta los tres ejemplos en orden.
2. Implementa los ejercicios sin mirar las soluciones.
3. Relaciona este módulo con **23_cedar_policies** para separar gobernanza y autorización fina.
4. Después continúa con **24_tools_management** para entender el ciclo de vida de las herramientas que el agente gobierna.
