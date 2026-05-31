# 🏢 Ask Sage Enterprise

## 📚 Descripción

La versión **enterprise** de Ask Sage toma el MVP y lo convierte en una plataforma confiable para múltiples organizaciones, equipos y áreas sensibles. Aquí aparecen responsabilidades nuevas: aislar datos por tenant, restringir acceso según roles, registrar auditoría, medir uso, monitorear SLA y evitar fallos en cascada con **circuit breakers**.

Este módulo muestra cómo evolucionar un sistema útil a uno gobernable. La dificultad ya no está solo en responder bien, sino en responder bien **al usuario correcto**, con **los datos correctos** y dejando un rastro verificable.

## 🎯 Objetivos de Aprendizaje

- [x] Diseñar aislamiento de datos por tenant
- [x] Aplicar RBAC sobre documentos y consultas
- [x] Registrar eventos de auditoría completos
- [x] Calcular métricas para dashboards administrativos
- [x] Entender circuit breakers y monitoreo de SLA
- [x] Extender RAG con enforcement de permisos
- [x] Identificar por qué un MVP no alcanza para enterprise

## 📁 Estructura del Módulo

```
41_ask_sage_enterprise/
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

## 🧠 Concepto: qué cambia al pasar a enterprise

```
Usuario -> Tenant -> RBAC -> RAG -> LLM
             |         |      |      |
             |         |      |      +--> Circuit breaker / SLA
             |         |      +----------> Reranking / decomposition
             |         +-----------------> Permisos por documento
             +---------------------------> Aislamiento de datos
                      \
                       +--> Audit log -> Analytics -> Dashboard admin
```

## 🕰️ Historia y contexto

Muchas plataformas internas nacen como demos exitosas y luego fallan en adopción porque no consideran gobierno ni cumplimiento. En entornos regulados, Ask Sage no puede ser solo “un chatbot con documentos”: debe respetar políticas de acceso, demostrar quién vio qué y sostener niveles mínimos de servicio.

## 🟢 Básico: aislamiento por tenant

```python
tenant_docs = {"acme": ["Manual comercial"], "globex": ["Playbook de compliance"]}
print(tenant_docs["acme"])
```

## 🟡 Intermedio: RBAC sobre documentos

```python
role_permissions = {"admin": {"read", "write", "audit"}, "viewer": {"read"}}
print("audit" in role_permissions["admin"])
```

## 🔴 Avanzado: pipeline enterprise completo

```python
failures = 0
if failures >= 3:
    print("Circuit breaker abierto: usar respuesta degradada")
```

## 🧪 Panorama de Ejemplos Prácticos

- **`examples/01_basico.py`**: almacén multi-tenant con aislamiento explícito.
- **`examples/02_intermedio.py`**: capa RBAC con roles y permisos por documento.
- **`examples/03_avanzado.py`**: flujo enterprise con auditoría, analytics y circuit breaker.

## 🏋️ Panorama de Ejercicios

- **Ejercicio 1**: implementar `TenantIsolation` para consultas por tenant.
- **Ejercicio 2**: sumar RBAC y validar permisos al buscar.
- **Ejercicio 3**: construir auditoría y analytics con detección simple de anomalías.

## ⚖️ Alternativas y comparaciones

| Enfoque | Ventajas | Desventajas | Cuándo usarlo |
|---|---|---|---|
| Tenant por columna | Simple y barato | Riesgo si olvidas filtros | SaaS pequeño |
| Tenant por base separada | Máximo aislamiento | Mayor costo operativo | Clientes regulados |
| RBAC clásico | Fácil de entender | Puede ser rígido | Roles bien definidos |
| ABAC | Muy flexible | Más difícil de explicar | Reglas por atributos |
| Circuit breaker | Evita cascadas de error | Requiere tuning | Dependencias externas inestables |

## 📚 Recursos

- Martin Fowler - Circuit Breaker: https://martinfowler.com/bliki/CircuitBreaker.html
- AWS SaaS Tenant Isolation: https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/tenant-isolation.html
- NIST RBAC Model: https://csrc.nist.gov/projects/role-based-access-control
- Python `collections`: https://docs.python.org/3/library/collections.html
- OpenTelemetry Concepts: https://opentelemetry.io/docs/concepts/

## 🔗 Próximos pasos

1. Compara este módulo con el MVP y detecta las responsabilidades nuevas.
2. Ejecuta los ejemplos y observa cómo cada capa agrega control.
3. Resuelve los ejercicios antes de diseñar un dashboard real.
4. Continúa con **42_deployment_aws** para aprender a operarlo en producción.
