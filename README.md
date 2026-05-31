# 🤖 Agentic Chat System: Full Stack Study Hub

> **Arquitectura de 4 Capas Integradas: Frontend → Orchestration → Runtime → Validation**

Este es un **hub de estudio universitario** completo sobre cómo construir un **sistema de chat IA con Generative UI** siguiendo la arquitectura moderna recomendada:
- 🎨 **Frontend:** Vercel AI SDK + Next.js
- 🧠 **Orchestration:** LangGraph (grafos ejecutables)
- ☁️ **Runtime:** AWS Bedrock AgentCore
- ✅ **Validation:** Testing de prompts + workflows + CI/CD

**New:** Ahora con documentación interactiva en Nextra + código Python ejecutable + suite de testing.

---

## 🎯 ¿Por Qué Este Hub Existe?

Hace 5 años, construir un agente de IA significaba escribir `if/else` anidados. LangGraph cambió todo: **te permite escribir grafos donde la IA "piensa en círculos" hasta encontrar la respuesta correcta**.

Este hub te prepara para construir sistemas como **Ask Sage** (del caso de uso farmacéutico), donde el agente puede:
- Consultar bases de datos
- Tomar decisiones automáticas
- Pausarse para aprobación humana
- Recordar contexto entre preguntas
- Todo sin reescribir lógica cada vez

---

## 📚 Estructura de Este Hub

Cada **módulo** sigue el mismo patrón de aprendizaje:

```
1️⃣ CONCEPTO       → ¿Qué es?
2️⃣ PARA QUÉ SIRVE → ¿Cuándo lo uso?
3️⃣ HISTORIA        → ¿Por qué se creó así?
4️⃣ EJEMPLOS BÁSICOS → Código funcional, paso a paso
5️⃣ EJERCICIOS      → Practica lo aprendido
```

### 🗂️ Módulos Disponibles (11 módulos = 4 Deep Dives)

#### 🧠 **BLOQUE 1: LangGraph (El Backend)**
| # | Módulo | Duración | Dificultad | Requisitos |
|---|--------|----------|-----------|-----------|
| **0** | [Fundamentos de Grafos](./modulos/00_fundamentos_grafos/) | 45 min | 🟢 Básica | Python |
| **1** | [El State (Estado Centralizado)](./modulos/01_state/) | 60 min | 🟢 Básica | Módulo 0 |
| **2** | [Nodos: Las Funciones del Grafo](./modulos/02_nodos/) | 75 min | 🟡 Intermedia | Módulo 1 |
| **3** | [Aristas: El Enrutamiento Inteligente](./modulos/03_aristas/) | 90 min | 🟡 Intermedia | Módulo 2 |
| **4** | [Checkpoints: Memoria y Persistencia](./modulos/04_checkpoints/) | 75 min | 🟡 Intermedia | Módulo 3 |

#### ☁️ **BLOQUE 2: AWS Bedrock AgentCore (La Infraestructura)** ⭐ *Tu jefe te pidió esto*
| # | Módulo | Duración | Dificultad | Requisitos |
|---|--------|----------|-----------|-----------|
| **5** | [Serverless y Runtime en AWS](./modulos/05_aws_bedrock/) | 60 min | 🟡 Intermedia | Módulos 0-4 |
| **6** | [AgentCore: Deployment y Seguridad](./modulos/06_aws_agentcore/) | 75 min | 🟡 Intermedia | Módulo 5 |

#### 🔌 **BLOQUE 3: Conexión de Datos (MCP y Multimodalidad)**
| # | Módulo | Duración | Dificultad | Requisitos |
|---|--------|----------|-----------|-----------|
| **7** | [Model Context Protocol (MCP)](./modulos/07_mcp/) | 75 min | 🟡 Intermedia | Módulos 1-4 |
| **8** | [Embeddings Multimodales](./modulos/08_multimodal/) | 90 min | 🔴 Avanzada | Módulo 7 |

#### 🎨 **BLOQUE 4: Frontend y UX con Vercel AI SDK** ⭐ *Tu jefe te pidió esto*
| # | Módulo | Duración | Dificultad | Requisitos |
|---|--------|----------|-----------|-----------|
| **9** | [Vercel AI SDK: Streaming Básico](./modulos/09_vercel_ai_sdk/) | 75 min | 🟡 Intermedia | Node.js, React |
| **10** | [Generative UI: La Magia](./modulos/10_frontend_streaming/) | 90 min | 🔴 Avanzada | Módulo 9 |

#### 🎯 **PROYECTO INTEGRADO**
| # | Módulo | Duración | Dificultad | Requisitos |
|---|--------|----------|-----------|-----------|
| **11** | [Proyecto Final: Ask Sage Completo](./modulos/11_proyecto_integrado/) | 180 min | 🔴 Avanzada | Todos los módulos |

---

## 🎯 Tu Camino de Aprendizaje (Personalizado para tu Rol)

Tu jefe te pidió que estudies **Vercel AI SDK** y **AWS AgentCore**. Aquí está el camino recomendado:

### 📍 Ruta Rápida (Si solo quieres esos dos)
1. Módulo 0-4: LangGraph (entiende el backend)
2. **Módulo 5-6: AWS AgentCore** ⭐ *Prioridad alta*
3. **Módulo 9-10: Vercel AI SDK** ⭐ *Prioridad alta*
4. Módulo 11: Integra todo

**Tiempo total:** ~12 horas

### 📍 Ruta Completa (Recomendada)
Sigue todos los módulos en orden (0-11). Así entiendes toda la arquitectura.

**Tiempo total:** ~20 horas

---

## 🚀 Cómo Usar Este Hub

### Opción A: Aprendizaje Lineal (Recomendado)
```bash
1. Lee README.md del Módulo 0
2. Ejecuta los ejemplos en examples/
3. Resuelve los ejercicios en exercises/
4. Pasa al módulo siguiente
```

### Opción B: Saltar a Conceptos Específicos
Si ya conoces un tema, puedes saltar directamente. Pero **recomendamos** empezar por el Módulo 0, aunque sea lo básico.

### Opción C: Solo Ejemplos
Si prefieres aprender viendo código:
```bash
cd modulos/01_state/examples/
python 01_state_basico.py
```

---

## 🚀 Cómo Usar Este Hub

### Opción A: Ver Documentación Web (Recomendado)

```bash
npm install      # Una sola vez
npm run dev      # Abre http://localhost:3000

# Verás sidebar interactivo con todos los módulos
# Búsqueda integrada, dark mode, responsive
```

### Opción B: Ejecutar Código Python

```bash
cd python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Ejecutar ejemplos
python modulos/10_fundamentos_grafos/examples/01_basico.py

# Correr tests
pytest validation/test_prompts.py -v
```

### Opción C: Ambos (Lo Mejor)

Terminal 1:
```bash
npm run dev    # Documentación en http://localhost:3000
```

Terminal 2:
```bash
cd python
source venv/bin/activate
pytest validation/ -v    # Tests ejecutando
```

---

## 📚 Estructura

```
agentic-chat-system-study-hub/
├── pages/                    # 🎨 Documentación Nextra
│   ├── frontend/
│   ├── orchestration/        # 🧠 LangGraph
│   ├── runtime/              # ☁️ AWS
│   ├── data/
│   └── validation/           # ✅ NEW: Testing
│
├── python/                   # 🐍 Código ejecutable
│   ├── modulos/              # 21 módulos de aprendizaje
│   ├── validation/           # NEW: Testing suite
│   │   ├── mock_llm.py
│   │   ├── test_prompts.py
│   │   ├── test_workflows.py
│   │   └── examples/
│   └── requirements.txt
│
├── package.json              # Next.js + Nextra
└── README.md (este archivo)
```

---

## 📖 Filosofía de Este Hub

Este hub es **opinionado**. Decidimos:

### ✅ Lo Que SÍ Hacemos
- Enseñar **LangGraph moderno** (v0.1.0+)
- Usar **Anthropic Claude** como LLM (es el que usamos en Ask Sage)
- Ejemplo real: **bot farmacéutico** (consulta stock, cancela órdenes, etc)
- Código **ejecutable** que funciona ahora
- Explicaciones en **español puro** (sin spanglish)
- Opinionado: decimos QUÉ usar, no "depende"

### ❌ Lo Que NO Hacemos
- No cubrimos LangChain básico (asumimos que sabes qué es un LLM)
- No explicamos cómo funciona internamente Claude (ese es otro curso)
- No enseñamos "mejores prácticas generales de Python" (asumimos Python junior)
- No somos neutrales: esta es la forma correcta de hacer esto

---

## 🎓 Cómo Estudiar Cada Módulo

### Paso 1: Lee el Concepto
```
📄 modulos/01_state/README.md
   └─ ¿Qué es State?
   └─ ¿Por qué no pasar variables?
   └─ Cómo LangGraph fusiona cambios
```

### Paso 2: Ejecuta Ejemplos
```bash
cd modulos/01_state/examples/
python 01_estado_basico.py      # Hola Mundo en LangGraph
python 02_estado_diccionario.py # State con diccionarios
python 03_estado_pydantic.py    # State con validación
```

### Paso 3: Lee el Código
- Cada `ejemploN.py` tiene comentarios explicativos
- Hay diagramas ASCII en README.md
- No es mágica, es lógica común

### Paso 4: Intenta Ejercicios
```
📝 modulos/01_state/exercises/
   └─ ejercicio_01.py (guiado)
   └─ ejercicio_02.py (desafío)
```

### Paso 5: Haz Cambios
- Modifica el código
- Quebralo a propósito
- Aprende por error

---

## 🧪 Verificar Que Todo Funciona

Después de instalar:

```bash
# Ejecutar test de configuración
python test_setup.py

# Si ves ✅ en todo, estás listo
```

---

## 📺 Formato de Contenido

Cada módulo tiene:

**`README.md`** (El corazón del aprendizaje)
- 1️⃣ Concepto (¿Qué es?)
- 2️⃣ Para qué sirve (¿Cuándo lo uso?)
- 3️⃣ Historia (¿Por qué se creó así?)
- Diagramas ASCII explicativos
- Links a ejemplos

**`examples/`** (Código que corre)
- `01_basico.py` - Versión más simple
- `02_intermedio.py` - Con más características
- `03_avanzado.py` - Caso real

**`exercises/`** (Para practicar)
- Enunciados claros
- Soluciones en `solutions/`

---

## 🎯 Tu Primer Paso Ahora

👉 **Ve a `modulos/00_fundamentos_grafos/`**

Toma 45 minutos. No esperes a "estar listo". La mejor forma de aprender es empezar.

```bash
cd modulos/00_fundamentos_grafos/
# Lee el README.md
# Ejecuta los ejemplos
# Intenta los ejercicios
```

---

## 📞 Preguntas Frecuentes

### P: ¿Necesito saber qué es un LLM?
**R:** Sí. Mínimo: "Es una red neuronal que predice la siguiente palabra". No necesitas matemática detrás.

### P: ¿Puedo saltarme módulos?
**R:** Depende. Módulo 2 (Nodos) casi no necesita Módulo 0. Pero Módulo 3 (Aristas) necesita Módulo 2.

### P: ¿Este hub es para Ask Sage?
**R:** Es la base. Ask Sage va mucho más allá (AWS, MCP, frontend). Pero empezamos aquí.

### P: ¿Cuánto tiempo toma todo?
**R:** ~8 horas total si sigues paso a paso. Varía si saltas módulos.

---

## 📄 Estructura del Repositorio

```
agentic-chat-system-study-hub/
├── README.md                           # Este archivo
├── requirements.txt                    # Dependencias
├── test_setup.py                       # Verificar instalación
└── modulos/
    ├── 00_fundamentos_grafos/
    │   ├── README.md                   # Teoría
    │   ├── examples/                   # Código ejecutable
    │   │   ├── 01_grafo_simple.py
    │   │   └── 02_grafo_inteligente.py
    │   ├── exercises/                  # Ejercicios
    │   │   ├── ejercicio_01.py
    │   │   └── ejercicio_02.py
    │   └── solutions/                  # Soluciones
    │       ├── ejercicio_01.py
    │       └── ejercicio_02.py
    ├── 01_state/
    ├── 02_nodos/
    ├── 03_aristas/
    ├── 04_checkpoints/
    └── 05_proyecto_final/
```

---

## 🎓 Objetivos de Aprendizaje

Después de completar este hub, vas a:

- ✅ Entender cómo funcionan los **grafos ejecutables**
- ✅ Diseñar **Estados compartidos** eficientemente
- ✅ Escribir **Nodos** que hagan tareas reales
- ✅ Crear **Aristas condicionales** que enruten inteligentemente
- ✅ Implementar **Checkpoints** para persistencia
- ✅ Construir un **agente farmacéutico completo**

---

## 🤝 Contribuciones

¿Encontraste un error? ¿Tienes una mejor explicación?

```bash
git branch mejora/modulo-1
# Edita archivos
git commit -m "Mejora en Módulo 1: explicación más clara"
git push origin mejora/modulo-1
# Abre un PR
```

---

## 📍 Roadmap Futuro

- [ ] Módulo 6: Deployment en AWS AgentCore
- [ ] Módulo 7: MCP (Model Context Protocol)
- [ ] Módulo 8: Streaming y Frontend (Vercel AI SDK)
- [ ] Ejercicios interactivos (Jupyter)
- [ ] Videotutoriales (YouTube)

---

## 📄 Licencia

Todo el contenido es **CC-BY-4.0**. Úsalo, cópialo, enseña con él.

---

**Última actualización:** Mayo 2026  
**Versión:** 1.0 (Initial Release)  
**Mantenedor:** NaN Labs Study Hub Team
