# 📑 ÍNDICE DE NAVEGACIÓN: Agentic Chat System Study Hub

> **Guía centralizada para navegación rápida por el estudio. Empieza aquí.**

---

## 🚀 INICIO RÁPIDO (15 minutos)

1. **¿Por qué este hub?** → Lee [QUICKSTART.md](./QUICKSTART.md)
2. **¿Cómo está estructurado?** → Lee [ARQUITECTURA.md](./ARQUITECTURA.md)
3. **¿Qué voy a aprender?** → Lee [README.md](./README.md)

---

## 📚 RUTA DE APRENDIZAJE RECOMENDADA

### 🎯 Opción 1: RUTA RÁPIDA (12-15 horas) ⭐ RECOMENDADA
*Para quien tiene tiempo limitado y prioridades claras*

```
Semana 1:
├─ Día 1: Vercel AI SDK (Módulos 00-01)     [2h]
│  └─ Intro + Streaming
├─ Día 2: AWS Basics (Módulo 20)            [1h]
│  └─ Serverless fundamentals
├─ Día 3-4: Identity Forwarding (Módulo 21) [1.5h] ⭐ PRIORIDAD
│  └─ Credenciales + ejemplos AWS
└─ Día 5: Governance (Módulo 22)            [1.5h] ⭐ PRIORIDAD
   └─ Cedar policies + ejercicios

Semana 2:
├─ Día 1-2: LangGraph basics (Módulos 10-11) [2h]
│  └─ Grafos + State
├─ Día 3: Proyecto MVP (Módulo 40)           [3h]
│  └─ Integración Vercel + LangGraph
└─ Día 4-5: Revisión + práctica             [2h]
```

**Total: ~14 horas**

### 🏢 Opción 2: RUTA COMPLETA (23.5 horas)
*Para quien quiere dominar todo el stack*

```
Semana 1-2:
├─ Fundamentos LangGraph (Módulos 10-14)     [5.75h]
├─ Frontend Vercel (Módulos 00-03)           [4.5h]
└─ AWS AgentCore (Módulos 20-24)             [6h]

Semana 3:
├─ Data Layer (Módulos 30-31)                [2.75h]
├─ Proyectos capstone (Módulos 40-42)        [4.5h]
└─ Ejercicios finales                        [2h]

Total: ~25 horas (sin ejercicios: ~23.5h)
```

---

## 🗂️ MÓDULOS ORGANIZADOS POR CAPA

### 🎨 CAPA 1: FRONTEND (Vercel AI SDK)
**Duración**: 4.5 horas | **Dificultad**: Básica → Intermedia

| # | Módulo | Tiempo | Estado | Link |
|---|--------|--------|--------|------|
| 00 | Intro a Vercel AI SDK | 45 min | ✅ Hecho | [ir →](./modulos/00_vercel_intro/) |
| 01 | Streaming de Tokens | 60 min | 📝 Estructura | [ir →](./modulos/01_streaming/) |
| 02 | Generative UI (Componentes) | 75 min | ✅ Hecho | [ir →](./modulos/02_generative_ui/) |
| 03 | Frontend Completo | 60 min | 📝 Estructura | [ir →](./modulos/03_frontend_completo/) |

**Tu próximo paso**: Abre [modulos/00_vercel_intro/](./modulos/00_vercel_intro/)

---

### 🧠 CAPA 2: ORCHESTRATION (LangGraph)
**Duración**: 5.75 horas | **Dificultad**: Básica → Intermedia

| # | Módulo | Tiempo | Estado | Link |
|---|--------|--------|--------|------|
| 10 | Fundamentos de Grafos | 45 min | ✅ Hecho | [ir →](./modulos/10_fundamentos_grafos/) |
| 11 | State (Estado Centralizado) | 60 min | 📝 Estructura | [ir →](./modulos/11_state/) |
| 12 | Nodos (Funciones del Grafo) | 75 min | 📝 Estructura | [ir →](./modulos/12_nodos/) |
| 13 | Aristas (Enrutamiento) | 90 min | 📝 Estructura | [ir →](./modulos/13_aristas/) |
| 14 | Checkpoints (Persistencia) | 75 min | 📝 Estructura | [ir →](./modulos/14_checkpoints/) |

**Tu próximo paso**: Lee [modulos/10_fundamentos_grafos/](./modulos/10_fundamentos_grafos/)

---

### ☁️ CAPA 3: RUNTIME (AWS AgentCore) ⭐ TU PRIORIDAD
**Duración**: 6 horas | **Dificultad**: Intermedia → Avanzada

| # | Módulo | Tiempo | Estado | Link | Prioridad |
|---|--------|--------|--------|------|-----------|
| 20 | Serverless Basics | 60 min | ✅ Hecho | [ir →](./modulos/20_serverless_basics/) | Media |
| 21 | Identity Forwarding | 75 min | ✅ Hecho | [ir →](./modulos/21_identity_forwarding/) | ⭐⭐⭐ |
| 22 | Governance con Cedar | 90 min | ✅ Hecho | [ir →](./modulos/22_agentcore_governance/) | ⭐⭐⭐ |
| 23 | Cedar Policies Avanzadas | 60 min | 📝 Estructura | [ir →](./modulos/23_cedar_policies/) | Media |
| 24 | Tools & Memory Management | 75 min | 📝 Estructura | [ir →](./modulos/24_tools_management/) | Media |

**⭐ EMPIEZA AQUÍ**: Lee [modulos/21_identity_forwarding/](./modulos/21_identity_forwarding/)

---

### 🔌 CAPA 4: DATA LAYER (MCP + Embeddings)
**Duración**: 2.75 horas | **Dificultad**: Intermedia → Avanzada

| # | Módulo | Tiempo | Estado | Link |
|---|--------|--------|--------|------|
| 30 | Model Context Protocol (MCP) | 75 min | 📝 Estructura | [ir →](./modulos/30_mcp_protocol/) |
| 31 | Embeddings Multimodales | 90 min | 📝 Estructura | [ir →](./modulos/31_multimodal_embeddings/) |

---

### 🎯 PROYECTOS FINALES (Integración Total)
**Duración**: 4.5 horas | **Dificultad**: Avanzada

| # | Proyecto | Tiempo | Estado | Link | Stack |
|---|----------|--------|--------|------|-------|
| 40 | Ask Sage MVP | 2h | 📝 Estructura | [ir →](./modulos/40_ask_sage_mvp/) | Vercel + LangGraph |
| 41 | Ask Sage Enterprise | 2h | 📝 Estructura | [ir →](./modulos/41_ask_sage_enterprise/) | Vercel + LangGraph + AgentCore |
| 42 | Deployment en AWS | 30 min | 📝 Estructura | [ir →](./modulos/42_deployment_aws/) | CI/CD + Bedrock |

---

## 📋 ARCHIVOS MAESTROS

### 🎯 Documentos de Orientación
| Archivo | Propósito | Tiempo | Cuándo leer |
|---------|-----------|--------|-----------|
| [QUICKSTART.md](./QUICKSTART.md) | Guía de inicio rápido | 10 min | **HOY - primero** |
| [ARQUITECTURA.md](./ARQUITECTURA.md) | Explicación de 4 capas | 15 min | **HOY - segundo** |
| [README.md](./README.md) | Descripción general | 10 min | **HOY - tercero** |

### 📖 Documentos de Referencia
| Archivo | Propósito | Cuándo usar |
|---------|-----------|-----------|
| [PLAN.md](./PLAN.md) | Plan original detallado | Como referencia técnica |
| [ROADMAP.md](./ROADMAP.md) | Timeline visual | Para entender progresión |
| [ANALISIS_REESTRUCTURACION.md](./ANALISIS_REESTRUCTURACION.md) | Por qué restructuramos | Si te preguntas por la estructura |
| [RESUMEN_EJECUTIVO.md](./RESUMEN_EJECUTIVO.md) | Resumen de lo creado | Para referencia ejecutiva |

---

## 🎓 ESTRUCTURA DE CADA MÓDULO

Cada módulo sigue este patrón (diseñado para aprendizaje universitario):

```
📁 modulos/NN_nombre_modulo/
├── README.md              # Contenido principal
│   ├─ 1. CONCEPTO       → ¿Qué es?
│   ├─ 2. PARA QUÉ SIRVE → ¿Cuándo lo uso?
│   ├─ 3. HISTORIA        → ¿Por qué se creó?
│   ├─ 4. EJEMPLOS        → Código funcional
│   └─ 5. EJERCICIOS      → Practica + soluciones
├── ejemplos/
│   ├── basico.py         # Ejemplo simple
│   ├── avanzado.py       # Ejemplo complejo
│   └── requirements.txt  # Dependencias específicas
└── ejercicios/
    ├── ejercicio_1.md    # Enunciado
    ├── solucion_1.py     # Solución
    └── ...
```

---

## 🚦 CÓMO NAVEGACIÓN FUNCIONA

### Desde la terminal:
```bash
# 1. Entra al hub
cd ~/Documents/projects/NanLabs/agentic-chat-system-study-hub

# 2. Lee el índice (este archivo)
cat INDEX.md

# 3. Elige tu ruta (rápida o completa)
# Ruta rápida: Ve a QUICKSTART.md
cat QUICKSTART.md

# 4. Sigue a un módulo
cd modulos/21_identity_forwarding/
cat README.md
```

### Desde un editor (VS Code / Cursor):
1. Abre la carpeta proyecto
2. Abre `INDEX.md` (este archivo)
3. Usa Cmd+Click o busca módulo por nombre
4. Los links son relativos (funcionan en VS Code)

---

## 🎯 TU JEFE TE PIDIÓ APRENDER

### **Vercel AI SDK**
- [x] Módulo 00: Intro a Vercel
- [x] Módulo 01: Streaming (en progreso)
- [x] Módulo 02: Generative UI

**Tiempo recomendado**: 2.5 horas

**Módulos clave**: 
- [modulos/00_vercel_intro/](./modulos/00_vercel_intro/) ← Comienza aquí
- [modulos/02_generative_ui/](./modulos/02_generative_ui/)

---

### **AWS AgentCore**
- [x] Módulo 20: Serverless Basics
- [x] Módulo 21: **Identity Forwarding** ⭐⭐⭐
- [x] Módulo 22: **Governance con Cedar** ⭐⭐⭐

**Tiempo recomendado**: 3.5 horas (es lo más importante)

**Módulos clave**:
- [modulos/21_identity_forwarding/](./modulos/21_identity_forwarding/) ← ⭐ PRIORITARIO
- [modulos/22_agentcore_governance/](./modulos/22_agentcore_governance/) ← ⭐ PRIORITARIO

---

## 💡 TIPS DE NAVEGACIÓN

### 📍 Si quieres aprender una capa completa:
1. Lee el README.md del primer módulo
2. Haz los ejercicios
3. Avanza al siguiente

### 🎯 Si tienes tiempo limitado:
1. Ve directo a [QUICKSTART.md](./QUICKSTART.md)
2. Sigue la "Ruta Rápida"
3. Enfócate en módulos 21 y 22 (tu jefe lo pidió)

### 🔄 Si vuelves después de un descanso:
1. Lee [ARQUITECTURA.md](./ARQUITECTURA.md) para contexto
2. Abre el módulo donde dejaste
3. Los ejercicios tienen soluciones comentadas

---

## 📊 ESTADÍSTICAS DEL HUB

- **Módulos totales**: 19 (+ 3 proyectos finales)
- **Módulos completados**: 6 (README.md + ejemplos)
- **Módulos en estructura**: 14 (listos para agregar contenido)
- **Archivos maestros**: 6 (orientación + referencia)
- **Horas totales de estudio**: ~23.5h (o 12-15h ruta rápida)
- **Idioma**: 100% Español
- **Nivel**: Universitario opinionado

---

## ✅ CHECKLIST: "HOY VOY A EMPEZAR"

```
Hoy mismo:
 [ ] Leer QUICKSTART.md (10 min)
 [ ] Leer ARQUITECTURA.md (15 min)
 [ ] Abrir modulos/00_vercel_intro/README.md (15 min)
 [ ] Ejecutar primer ejemplo (20 min)

Mañana:
 [ ] Terminar módulo 00 + ejercicios (45 min)
 [ ] Empezar módulo 21 Identity Forwarding (90 min)

Esta semana:
 [ ] Completar módulos 21 y 22 (3 horas)
 [ ] Hacer ejercicios de ambos
 [ ] Entender cómo funciona la arquitectura completa
```

---

## 🆘 SI TE PIERDES

1. **¿No sé qué módulo ver primero?**
   → Lee [QUICKSTART.md](./QUICKSTART.md)

2. **¿No entiendo cómo conecta todo?**
   → Lee [ARQUITECTURA.md](./ARQUITECTURA.md)

3. **¿Qué debo aprender primero?**
   → Sigue [README.md](./README.md) recomendaciones

4. **¿Cuál es mi prioridad?**
   → Módulos 21 (Identity) y 22 (Governance) - tu jefe lo pidió

5. **¿Cuánto tiempo es?**
   → Ruta rápida: 12-15h | Ruta completa: 23.5h

---

## 🔗 LINKS RÁPIDOS

**Empieza aquí:**
- [QUICKSTART.md](./QUICKSTART.md) - 10 minutos
- [ARQUITECTURA.md](./ARQUITECTURA.md) - 15 minutos

**Tu prioridad (tu jefe te pidió):**
- [modulos/21_identity_forwarding/](./modulos/21_identity_forwarding/) - Identity
- [modulos/22_agentcore_governance/](./modulos/22_agentcore_governance/) - Governance

**Módulo 1 (Vercel Frontend):**
- [modulos/00_vercel_intro/](./modulos/00_vercel_intro/)

**Módulo de Grafos (LangGraph):**
- [modulos/10_fundamentos_grafos/](./modulos/10_fundamentos_grafos/)

---

## 📞 NOTAS FINALES

- Este hub es **opinionado**: no enseña todas las opciones, enseña las mejores
- Los módulos incluyen **ejemplos ejecutables** que puedes copiar
- Hay **ejercicios resueltos** para practicar
- Todo está en **español puro** (sin Spanglish)
- El hub es **progresivo**: cada módulo construye sobre los anteriores

**Siguiente paso**: Abre [QUICKSTART.md](./QUICKSTART.md)

---

*Última actualización: 2026-05-29*
*Hub: Agentic Chat System Study Hub v2.0*
*Ubicación: ~/Documents/projects/NanLabs/agentic-chat-system-study-hub/*
