# 🌲 Control de Acceso con Cedar Policy Language

## 📚 Descripción

**Cedar** es un lenguaje de políticas open source creado por AWS para expresar autorización fina de forma legible, auditable y segura. En lugar de esconder permisos dentro de `if/else` dispersos por la aplicación, Cedar separa la decisión de acceso en reglas explícitas basadas en el modelo **PARC: Principal, Action, Resource, Context**.

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- [ ] Explicar qué es Cedar y por qué aparece en sistemas modernos de autorización.
- [ ] Aplicar el modelo PARC a decisiones de acceso reales.
- [ ] Entender la diferencia entre reglas `permit` y `forbid`.
- [ ] Implementar evaluación de políticas con precedencia de denegación explícita.
- [ ] Modelar grupos, jerarquías de recursos y condiciones de contexto.
- [ ] Comparar Cedar con RBAC, ABAC y OPA/Rego.

## 📋 Estructura del Módulo

```text
23_cedar_policies/
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

## 🧠 El Modelo PARC

Cedar evalúa solicitudes de acceso en torno a cuatro piezas.

```text
+-----------+   quiere hacer   +---------+
| Principal | ----------------> | Action |
+-----------+                   +---------+
      |                               |
      | sobre                         | en presencia de
      v                               v
+-----------+  con atributos      +-----------+
| Resource  | <------------------ | Context   |
+-----------+                     +-----------+
```

- **Principal**: quién solicita la acción.
- **Action**: qué intenta hacer.
- **Resource**: sobre qué objeto actúa.
- **Context**: condiciones externas como IP, tenant, horario o región.

## 🕰️ Historia y Contexto

Durante años, muchas aplicaciones resolvieron permisos con RBAC rígido: roles fijos como `admin`, `editor`, `viewer`. Ese modelo es útil, pero se queda corto cuando necesitas condiciones más finas: “un analista puede leer reportes del tenant X solo dentro del horario laboral y desde IP corporativa”.

AWS creó Cedar para responder a ese problema de forma segura y auditable, y lo convirtió en la base conceptual de **Amazon Verified Permissions**. La propuesta combina claridad sintáctica, separación entre policy store y aplicación, y una semántica donde **`forbid` explícito gana siempre**.

## 🟢 Nivel Básico: Evaluador Tipo Cedar

El primer paso es entender la mecánica de `permit` y `forbid`.

```python
policy = {
    "effect": "permit",
    "principal": "user:ana",
    "action": "read",
    "resource": "doc:manual",
}
```

Luego comparas una solicitud `(principal, action, resource)` contra el conjunto de reglas.

## 🟡 Nivel Intermedio: Grupos y Jerarquías

En la práctica, los usuarios heredan permisos por grupo y los recursos suelen formar árboles.

```python
principal_groups = {"user:ana": ["group:analysts"]}
resource_parents = {"doc:q2": "folder:finance"}
```

Eso permite escribir políticas más reutilizables: autorizas un grupo sobre una carpeta y heredas a todos los documentos debajo.

## 🔴 Nivel Avanzado: Contexto + Auditoría

La autorización madura no se limita a identidad; también evalúa contexto y deja trazabilidad.

```python
request = {
    "principal": "user:ana",
    "action": "read",
    "resource": "doc:q2",
    "context": {"tenant": "acme", "ip": "10.0.0.15", "time": "10:30"},
}
```

Aquí el motor puede revisar políticas, jerarquías de entidades y razones de la decisión final.

## 💼 Panorama de Ejemplos Prácticos

- **`examples/01_basico.py`**: evaluador simple con `permit` y `forbid`.
- **`examples/02_intermedio.py`**: agrega grupos, herencia y condiciones por contexto.
- **`examples/03_avanzado.py`**: construye un servicio de autorización con auditoría.

## 🧪 Panorama de Ejercicios

- **Ejercicio 1**: crear un `PolicyStore` para triples básicos.
- **Ejercicio 2**: heredar permisos desde grupos.
- **Ejercicio 3**: evaluar contexto como horario e IP.

## 🔀 Alternativas y Comparación

| Enfoque | Fortalezas | Debilidades | Caso típico |
|---|---|---|---|
| **Cedar** | Políticas legibles, deny explícito, buen fit con Verified Permissions | Nuevo para muchos equipos | Autorización fina en apps modernas |
| **RBAC clásico** | Fácil de entender | Poca granularidad | Backoffice simple con pocos roles |
| **ABAC ad hoc** | Flexible con atributos | Suele dispersarse por el código | Sistemas que crecieron sin policy engine |
| **OPA / Rego** | Muy expresivo y generalista | Rego puede ser más difícil de dominar | Plataformas con policy-as-code transversal |
| **XACML** | Muy potente y estandarizado | Verboso y pesado | Entornos enterprise legacy |

## 📚 Recursos

- Sitio oficial de Cedar: https://www.cedarpolicy.com/en
- Cedar GitHub: https://github.com/cedar-policy/cedar
- Amazon Verified Permissions: https://docs.aws.amazon.com/verifiedpermissions/latest/userguide/what-is-avp.html
- Cedar language reference: https://docs.cedarpolicy.com/
- AWS Security Blog sobre autorización fina: https://aws.amazon.com/blogs/security/

## ⏭️ Próximos Pasos

1. Ejecuta el evaluador básico y observa la precedencia de `forbid`.
2. Relaciona Cedar con **22_agentcore_governance**: gobernanza decide “qué puede hacer el agente”; Cedar ayuda a decidir “qué puede hacer un principal sobre un recurso”.
3. Continúa con **24_tools_management** para conectar autorización con invocación real de herramientas.
