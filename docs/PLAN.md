# 📋 PLAN GENERAL: Estructura Completa del Hub

## 🧭 Visión General

Este hub cubre todo lo necesario para construir **Ask Sage**, un agente farmacéutico inteligente. La arquitectura es:

```
┌─────────────────────────────────────────────────────────────────┐
│                        USUARIO FINAL (Celular)                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │ Frontend React      │
                    │ (Módulos 9-10)      │
                    │ + Vercel AI SDK     │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │  Next.js API Route  │
                    │ (Streaming Text)    │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
    ┌────▼─────┐        ┌──────▼──────┐       ┌─────▼────┐
    │ LangGraph │        │ AWS Bedrock │       │ MCP      │
    │ (Módulos  │        │ AgentCore   │       │ Servers  │
    │  0-4)     │        │ (Módulos5-6)│       │(Módulo 7)│
    └────┬─────┘        └──────┬──────┘       └─────┬────┘
         │                     │                     │
    ┌────▼─────────────────────┴─────────────────────▼────┐
    │          Bases de Datos, APIs, Servicios            │
    │  • SQL: Stock, Órdenes, Usuarios                    │
    │  • Embeddings: Videos, PDFs (Módulo 8)              │
    │  • Servicios: Payment, Shipping, etc                │
    └────────────────────────────────────────────────────┘
```

---

## 📚 Los 4 Deep Dives

### 🧠 **Deep Dive 1: LangGraph (El Backend)**
**Módulos:** 0, 1, 2, 3, 4

**Qué aprendes:**
- Cómo estructurar agentes con **States compartidos**
- Escribir **Nodos** que hacen tareas reales
- Crear **Aristas condicionales** que enrutan flujos
- Implementar **Checkpoints** para persistencia

**Por qué importa:**
- Es donde vive toda la lógica del agente
- Define cómo el LLM toma decisiones
- Todo lo demás (AWS, frontend) depende de esto

**Duración:** ~5 horas

---

### ☁️ **Deep Dive 2: AWS Bedrock AgentCore (La Infraestructura)** ⭐
**Módulos:** 5, 6

**Qué aprendes:**
- **Serverless runtime**: Cómo sube el código a AWS
- **Identity Forwarding**: Cómo se pasan credenciales del usuario
- **Cedar Policies**: Control de seguridad integrado
- Deployment con `agentcore deploy`

**Por qué importa (es prioritario):**
- Esto es la REALIDAD: LangGraph local es solo desarrollo
- AWS es donde vive en PRODUCCIÓN
- Security = Identity Forwarding = Tu trabajo

**Duración:** ~2.5 horas

**⚠️ IMPORTANTE:** Módulos 5-6 son más conceptuales (no puedes testear AWS sin credenciales), pero tienen pseudo-código que emulas localmente.

---

### 🔌 **Deep Dive 3: Conexión de Datos (MCP y Multimodalidad)**
**Módulos:** 7, 8

**Qué aprendes:**
- **MCP (Model Context Protocol)**: Estándar abierto para exponer datos
- Crear servidores MCP reutilizables
- **Embeddings multimodales**: Buscar en videos/fotos
- Ingestión de datos

**Por qué importa:**
- Evita hardcodear conexiones a BD
- MCP = "USB-C de la IA"
- Reutilizable entre agentes

**Duración:** ~2.5 horas

---

### 🎨 **Deep Dive 4: Frontend y UX con Vercel AI SDK** ⭐
**Módulos:** 9, 10

**Qué aprendes:**
- **streamText**: Streaming de tokens en tiempo real
- Hook `useChat` en React
- **Generative UI**: Backend envía componentes React
- Serialización de RSC (React Server Components)

**Por qué importa (es prioritario):**
- Es donde el usuario VE el agente
- Diferencia entre UX mediocre y excelente
- Vercel AI SDK es el estándar moderno

**Duración:** ~3 horas

---

### 🎯 **Proyecto Final: Ask Sage Integrado**
**Módulo:** 11

**Qué construyes:**
- Un agente farmacéutico COMPLETO
- Backend + Frontend + Seguridad
- Que funciona end-to-end

**Duración:** ~3 horas

---

## 🗺️ Dependencias Entre Módulos

```
Módulo 0 (Grafos)
    ↓
Módulo 1 (State) ──→ Módulo 7 (MCP)
    ↓                    ↓
Módulo 2 (Nodos) ─→ Módulo 8 (Multimodal)
    ↓
Módulo 3 (Aristas)
    ↓
Módulo 4 (Checkpoints)
    ↓
Módulo 5 (AWS Serverless)
    ↓
Módulo 6 (AWS AgentCore)
    ↓
Módulo 9 (Vercel AI SDK - Frontend)
    ↓
Módulo 10 (Generative UI)
    ↓
Módulo 11 (Proyecto Final)
```

---

## 📖 Patrón de Cada Módulo

Cada módulo SIEMPRE tiene:

```
modulos/0X_nombre/
├── README.md               # El corazón
│   ├── 1️⃣ CONCEPTO
│   ├── 2️⃣ PARA QUÉ SIRVE
│   ├── 3️⃣ HISTORIA
│   ├── 4️⃣ EJEMPLOS (con salida esperada)
│   └── 5️⃣ EJERCICIOS (con links a solutions)
├── examples/
│   ├── 01_basico.py
│   ├── 02_intermedio.py
│   └── 03_avanzado.py
├── exercises/
│   ├── ejercicio_01.py
│   ├── ejercicio_02.py
│   └── ejercicio_03.py
└── solutions/
    ├── ejercicio_01_solution.py
    ├── ejercicio_02_solution.py
    └── ejercicio_03_solution.py
```

### Garantías de Este Hub

✅ **Cada ejemplo corre sin errores**
✅ **Cada ejercicio tiene solución**
✅ **Todo está en español puro**
✅ **Es opinionado** (decimos qué usar, no "depende")
✅ **Progresivo** (fácil → difícil)

---

## 🎯 Objetivos de Aprendizaje Finales

Al terminar este hub, serás capaz de:

1. **Arquitectura:**
   - Diseñar grafos complejos con ciclos
   - Estructurar estados eficientemente
   - Entender flujo de datos de punta a punta

2. **Backend:**
   - Escribir agentes en LangGraph
   - Deployar en AWS AgentCore
   - Implementar seguridad con Identity Forwarding

3. **Datos:**
   - Crear servidores MCP
   - Procesar embeddings multimodales
   - Integrar bases de datos vectoriales

4. **Frontend:**
   - Streaming en tiempo real
   - Generative UI (componentes dinámicos)
   - UX de chatbots modernos

5. **End-to-End:**
   - Construir un agente farmacéutico completo
   - Que funciona en AWS
   - Con frontend en React

---

## ⏱️ Estimado de Tiempo

| Bloque | Módulos | Horas | Requiere AWS |
|--------|---------|-------|-------------|
| LangGraph | 0-4 | 5 | ❌ |
| AWS AgentCore | 5-6 | 2.5 | ⚠️ (Conceptual) |
| MCP | 7-8 | 2.5 | ❌ |
| Vercel AI SDK | 9-10 | 3 | ❌ |
| Proyecto Final | 11 | 3 | ⚠️ (Pseudo-deploy) |
| **TOTAL** | **0-11** | **~16 horas** | - |

---

## 🎓 Recomendaciones por Rol

### 👨‍💻 Backend Developer (tu caso probablemente)
**Ruta:** 0-4 → 5-6 (prioritario) → 7-8 → 11
**Énfasis:** LangGraph + AWS
**Skip:** Módulos 9-10 (pero léelos)
**Tiempo:** ~10 horas

### 🎨 Frontend Developer
**Ruta:** 0 (entender conceptos) → 9-10 (prioritario) → 11
**Énfasis:** Vercel AI SDK + React
**Skip:** Módulos 5-6 (pero léelos)
**Tiempo:** ~6 horas

### 🎯 Full-Stack / DevOps
**Ruta:** 0-11 (completo)
**Énfasis:** Todo
**Skip:** Nada
**Tiempo:** ~16 horas

---

## 🚀 Próximos Pasos

1. **HOY:** Lee este documento (este que estás leyendo)
2. **Mañana:** Comienza Módulo 0 (45 minutos)
3. **Semana 1:** Módulos 0-4 (Backend LangGraph)
4. **Semana 2:** Módulos 5-6 (AWS - es prioritario)
5. **Semana 2-3:** Módulos 7-10 (Datos + Frontend)
6. **Final:** Módulo 11 (Proyecto integrado)

---

## 📞 Estructura de Archivos del Hub

```
langgraph-study-hub/
├── README.md                              # Inicio
├── PLAN.md                                # Este archivo
├── requirements.txt                       # Dependencias
├── test_setup.py                          # Verificar instalación
│
├── modulos/
│   ├── 00_fundamentos_grafos/
│   │   ├── README.md
│   │   ├── examples/
│   │   ├── exercises/
│   │   └── solutions/
│   │
│   ├── 01_state/                         # Módulo State
│   ├── 02_nodos/
│   ├── 03_aristas/
│   ├── 04_checkpoints/
│   │
│   ├── 05_aws_bedrock/                   # ⭐ La arquitectura requiere AWS
│   ├── 06_aws_agentcore/
│   │
│   ├── 07_mcp/
│   ├── 08_multimodal/
│   │
│   ├── 09_vercel_ai_sdk/                 # ⭐ La arquitectura requiere Vercel
│   ├── 10_frontend_streaming/
│   │
│   └── 11_proyecto_integrado/
│
├── assets/                                # Diagramas, imágenes
│   ├── langgraph_architecture.png
│   └── ask_sage_flow.png
│
└── .env.example                           # Variables de entorno
```

---

## ✍️ Notas Finales

### Por Qué Este Hub Es Especial

1. **Opinionado**: No dice "puedes usar X o Y". Dice "usa X".
2. **Español**: Todo en español, sin mezclas
3. **Ejecutable**: Todo el código corre AHORA
4. **Progresivo**: Empieza fácil, termina con un proyecto real
5. **Enfocado**: Específico para Ask Sage, no genérico

### Lo Que NO Es

- ❌ No es documentación oficial de LangGraph (eso existe en docs.langgraph.com)
- ❌ No es tutorial de Python (asumimos Python basic)
- ❌ No es curso de ML (no enseñamos matemática)
- ❌ No es "imparcial" (somos opinionados a propósito)

### Consejo Final

> **No intentes terminar todo de una vez.** 
> 
> Este hub está diseñado para estudiantes. Toma 30-45 minutos por sesión, haz un ejercicio, camina, regresa mañana.
> 
> La mejor forma de aprender es **hacer**, no **leer**.

---

**Creado con ❤️ para el estudio integral de sistemas agentic.**

**Versión:** 1.0  
**Última actualización:** Mayo 2026
