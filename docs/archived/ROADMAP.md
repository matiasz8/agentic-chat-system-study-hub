# 🗺️ ROADMAP VISUAL: Estructura Completa del Hub

> Guía rápida para entender qué estudiar, cuándo, y en qué orden.

---

## 📊 Los 4 Deep Dives (La Arquitectura Completa)

```
┌──────────────────────────────────────────────────────────────────┐
│                        USUARIO FINAL                            │
│                    (Celular / Navegador)                        │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│              🎨 FRONTEND (Módulos 9-10)                          │
│        React + Next.js + Vercel AI SDK                          │
│                                                                  │
│  • Streaming de tokens (Módulo 9)                              │
│  • Generative UI - componentes dinámicos (Módulo 10)           │
│  • Chat interactivo, gráficos, formularios                     │
│  • Indica "Escribir", "Pensar", "Ejecutar"                     │
└──────────────┬───────────────────────────────────────────────────┘
               │
               │ API Calls
               │ 1. POST /api/chat
               │ 2. Headers: x-user-token
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│          ☁️ INFRAESTRUCTURA (Módulos 5-6)                        │
│     AWS Bedrock AgentCore + Identity Forwarding                 │
│                                                                  │
│  • Serverless Runtime (Módulo 5)                               │
│  • AWS AgentCore (Módulo 6)                                    │
│  • Identity Forwarding (inyecta user_token)                    │
│  • Cedar Policies (seguridad externa)                          │
│  • Checkpoints en DynamoDB                                     │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│           🧠 BACKEND (Módulos 0-4)                               │
│     LangGraph: Orquestación de Agentes                          │
│                                                                  │
│  • Módulo 0: Fundamentos de Grafos                             │
│  • Módulo 1: El State (estado centralizado)                    │
│  • Módulo 2: Nodos (funciones independientes)                  │
│  • Módulo 3: Aristas (enrutamiento inteligente)                │
│  • Módulo 4: Checkpoints (persistencia)                        │
│                                                                  │
│  Flujo:                                                         │
│    Usuario → Agent Node → Router (decision)                    │
│                    ↓                                            │
│         Query DB ← ← ← ← → Call LLM                           │
│                    ↓                                            │
│         Agent Node (resume)                                    │
│                    ↓                                            │
│         Respuesta al usuario                                   │
└──────────────┬───────────────────────────────────────────────────┘
               │
        ┌──────┴──────┬──────────────┐
        │             │              │
        ▼             ▼              ▼
    ┌────────┐   ┌────────────┐  ┌─────────┐
    │   🔌   │   │     MCP    │  │Multimodal
    │  Datos │   │ (Módulo 7) │  │(Módulo8)
    │   &    │   │            │  │
    │  APIs  │   │ Servidores │  │Embeddings
    └────────┘   │ Reutilizables│ │Vectoriales
                 └────────────┘  └─────────┘
```

---

## ⏱️ Timeline Recomendado

### 🟢 Ruta Rápida (Tu Jefe Pidió AWS + Vercel) - **10 horas**

```
LUNES       MARTES        MIÉRCOLES     JUEVES        VIERNES
───────     ───────       ───────       ───────       ───────

LangGraph   AWS Bedrock   MCP           Vercel AI    Proyecto
(3h)        (2h)          (2h)          SDK (2h)     Final
                                                     (1h)
Módulos:    Módulos:      Módulos:      Módulos:     Módulo:
0,1,2,3,4   5,6           7,8           9,10         11
```

**Orden:**
1. Entiende LangGraph (Módulos 0-4) - **NO puedes saltarte**
2. Entiende AWS (Módulos 5-6) - **Es prioritario**
3. Conoce MCP (Módulos 7-8) - **Mejor arquitectura**
4. Frontend (Módulos 9-10) - **Es prioritario**
5. Integra todo (Módulo 11) - **Verifica que funciona**

---

### 🟡 Ruta Completa (Recomendada) - **16 horas**

```
SEMANA 1           SEMANA 2
───────────        ───────────
LangGraph          AWS + MCP
(5 horas)          (6 horas)

SEMANA 3           SEMANA 4
───────────        ───────────
Vercel AI SDK      Proyecto
(3 horas)          (3 horas)

Módulos: 0-4 → 5-6 → 7-8 → 9-10 → 11
```

---

## 📚 Estructura de Carpetas

```
langgraph-study-hub/
│
├── 📄 README.md                    ← EMPIEZA AQUÍ
├── 📄 PLAN.md                      ← Visión general
├── 📄 ROADMAP.md                   ← Este archivo
├── 📄 requirements.txt
├── 🧪 test_setup.py
│
└── modulos/
    │
    ├── 🧠 00_fundamentos_grafos/      (45 min)
    │   ├── README.md
    │   ├── examples/
    │   │   ├── 01_grafo_simple.py
    │   │   └── 02_grafo_condicional.py
    │   ├── exercises/
    │   │   ├── ejercicio_01.py
    │   │   └── ejercicio_02.py
    │   └── solutions/
    │
    ├── 🧠 01_state/                   (60 min)
    │   ├── README.md
    │   ├── examples/
    │   └── exercises/
    │
    ├── 🧠 02_nodos/                   (75 min)
    ├── 🧠 03_aristas/                 (90 min)
    ├── 🧠 04_checkpoints/             (75 min)
    │
    ├── ☁️ 05_aws_bedrock/             (60 min) ⭐
    ├── ☁️ 06_aws_agentcore/           (75 min) ⭐
    │
    ├── 🔌 07_mcp/                     (75 min)
    ├── 🔌 08_multimodal/              (90 min)
    │
    ├── 🎨 09_vercel_ai_sdk/           (75 min) ⭐
    ├── 🎨 10_frontend_streaming/      (90 min) ⭐
    │
    └── 🎯 11_proyecto_integrado/      (180 min)
        ├── README.md
        └── ask_sage_completo/
```

---

## 🎯 Qué Aprendes en Cada Sección

### 🧠 BLOQUE 1: LangGraph (El Backend del Agente)

| Módulo | Concepto | Lo Que Haces |
|--------|----------|-------------|
| 0 | **Grafos 101** | Dibujas tu primer grafo en papel |
| 1 | **State** | Creas un objeto centralizado con todo el contexto |
| 2 | **Nodos** | Escribes funciones que hacen tareas |
| 3 | **Aristas** | Programas decisiones: "Si A, ir a B" |
| 4 | **Checkpoints** | Guardas estado en BD para pausar/reanudar |

**Resultado:** Un agente farmacéutico que funciona localmente

---

### ☁️ BLOQUE 2: AWS (La Infraestructura Profesional)

| Módulo | Concepto | Lo Que Haces |
|--------|----------|-------------|
| 5 | **Serverless** | Entiendes que AWS crea instancias bajo demanda |
| 6 | **AgentCore** | Subes tu agente a AWS con seguridad integrada |

**Resultado:** Tu agente corre en AWS con Identity Forwarding y Cedar Policies

---

### 🔌 BLOQUE 3: Datos (La Plomería)

| Módulo | Concepto | Lo Que Haces |
|--------|----------|-------------|
| 7 | **MCP** | Creas servidores reutilizables para datos |
| 8 | **Multimodal** | Procesas videos/fotos con embeddings |

**Resultado:** Tu agente puede consultar PDFs, videos, bases de datos

---

### 🎨 BLOQUE 4: Frontend (La Cara Visible)

| Módulo | Concepto | Lo Que Haces |
|--------|----------|-------------|
| 9 | **Streaming** | Respuestas llegan token por token |
| 10 | **Generative UI** | El backend envía gráficos/formularios |

**Resultado:** Un chat que se ve profesional y rápido

---

### 🎯 BLOQUE 5: Integración

| Módulo | Qué Hace |
|--------|----------|
| 11 | **Proyecto Final** - Todo junto: LangGraph + AWS + Frontend |

---

## 🚦 Requisitos por Módulo

### Módulos 0-4 (LangGraph - Backend)
```
✅ Python 3.10+
✅ pip (gestor de paquetes)
✅ Conocimiento BÁSICO de programación
✅ Editor de texto (VSCode recomendado)
```

### Módulos 5-6 (AWS)
```
✅ Módulos 0-4 completados
✅ Cuenta AWS (gratis por 12 meses)
✅ AWS CLI configurado
❌ NO necesitas credenciales reales (conceptual)
```

### Módulos 7-8 (MCP)
```
✅ Módulos 0-4 completados
✅ ffmpeg (para video)
✅ Pydantic (tipos)
```

### Módulos 9-10 (Vercel AI SDK)
```
✅ Node.js 18+
✅ React conocimientos básicos
✅ TypeScript básico
✅ Next.js básico
```

### Módulo 11 (Proyecto Final)
```
✅ TODOS los módulos anteriores
✅ 3-4 horas libres
✅ Café ☕
```

---

## ✨ Features del Hub

### ✅ Lo Que Tendrás

- [x] **11 módulos progresivos** con ejemplos funcionando
- [x] **Todo en español puro** (sin spanglish)
- [x] **Opinionado** - decimos QUÉ usar, no "depende"
- [x] **Ejemplos ejecutables** - copia/pega y funciona
- [x] **Ejercicios resueltos** - aprende haciendo
- [x] **Diagramas ASCII** - visualización clara
- [x] **Casos reales** - Ask Sage farmacéutico

### ❌ Lo Que NO Tendrás

- [ ] Videotutoriales (futuro)
- [ ] Explicación de matemática de LLMs
- [ ] Cómo configurar AWS desde cero
- [ ] "Las 5 mejores prácticas" (somos opinionados)

---

## 🎓 Objetivos de Aprendizaje

### Después del Módulo 4 (Fin de LangGraph)
- ✅ Entender qué es un grafo y por qué importa
- ✅ Diseñar un State eficiente
- ✅ Escribir nodos que llaman LLMs y BDs
- ✅ Crear aristas condicionales
- ✅ Implementar persistencia con checkpoints

### Después del Módulo 6 (Fin de AWS)
- ✅ Entender Serverless y sus límites
- ✅ Conocer Identity Forwarding
- ✅ Escribir políticas Cedar
- ✅ Saber cuándo usar AgentCore vs Lambda

### Después del Módulo 8 (Fin de Datos)
- ✅ Crear servidores MCP reutilizables
- ✅ Procesar embeddings multimodales
- ✅ Integrar BDs vectoriales

### Después del Módulo 10 (Fin de Frontend)
- ✅ Implementar streaming en React
- ✅ Usar Generative UI para interfaz dinámica
- ✅ Manejar estados de carga

### Después del Módulo 11 (Proyecto Final)
- ✅ **Construir un agente farmacéutico completo**
- ✅ Que funciona end-to-end
- ✅ Con seguridad, persistencia, UX

---

## 🎬 Próximos Pasos

### AHORA (5 minutos)
1. Lee este archivo completamente
2. Abre `modulos/00_fundamentos_grafos/README.md`
3. Estima el tiempo que tienes disponible

### HOY (45 minutos)
```bash
cd modulos/00_fundamentos_grafos/
# Lee el README.md
# Ejecuta los ejemplos
# Intenta los ejercicios
```

### ESTA SEMANA
```bash
# Módulos 1-4 (LangGraph)
cd modulos/01_state/ && # 60 min
cd modulos/02_nodos/ && # 75 min
cd modulos/03_aristas/ && # 90 min
cd modulos/04_checkpoints/ # 75 min
```

### PRÓXIMA SEMANA
```bash
# Módulos 5-6 (AWS)
cd modulos/05_aws_bedrock/ && # 60 min (conceptual)
cd modulos/06_aws_agentcore/ # 75 min (conceptual)
```

### SEMANA 3
```bash
# Módulos 7-8 (Datos)
cd modulos/07_mcp/ && # 75 min
cd modulos/08_multimodal/ # 90 min
```

### SEMANA 4
```bash
# Módulos 9-10 (Frontend)
cd modulos/09_vercel_ai_sdk/ && # 75 min
cd modulos/10_frontend_streaming/ # 90 min
```

### FINAL
```bash
# Módulo 11 (Proyecto)
cd modulos/11_proyecto_integrado/ # 3 horas
```

---

## ❓ FAQs

**P: ¿Cuánto tiempo toma todo?**
R: 16 horas si vas lento. 10 horas si salteas algunos. Recomendamos no saltarse nada.

**P: ¿Puedo hacer esto en 2 días?**
R: No. Tu cerebro necesita procesar. Dedica 2-3 horas diarias, tómate descansos.

**P: ¿Es difícil?**
R: Módulos 0-4 son fáciles. Módulos 5-10 son intermedios. Módulo 11 es challenging pero guiado.

**P: ¿Necesito AWS realmente?**
R: No para aprender. Pero sí para producción. Módulos 5-6 son conceptuales primero.

**P: ¿Funciona en Windows?**
R: Sí. Reemplaza `source venv/bin/activate` con `venv\Scripts\activate`

---

## 📞 Contacto

Si encontraste un error:
```bash
git branch mejora/mi-fix
# Edita archivos
git commit -m "Mejora en Módulo X"
git push origin mejora/mi-fix
# Abre un PR
```

---

## 🎉 ¡Estás Listo!

Te espera un viaje de 16 horas que te convertirá en experto en agentes de IA modernos.

**Próximo paso:**
```bash
cd modulos/00_fundamentos_grafos/
cat README.md
```

**Buena suerte.** 🚀

---

**Creado con ❤️ por NaN Labs Study Hub**  
**Versión:** 1.0  
**Última actualización:** Mayo 2026
