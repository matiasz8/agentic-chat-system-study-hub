# 🤝 Contributing to Agentic Hub

Cómo contribuir a este hub de estudio.

---

## 🎯 Antes de Empezar

Este es un **hub de estudio** (no un production app). Nuestro objetivo:
- Enseñar correctamente
- Mantener código limpio y comentado
- Ejemplos que funcionen
- Tests para validación

---

## 📋 Cómo Agregar un Nuevo Módulo

### Paso 1: Crear Carpeta

```bash
mkdir python/modulos/XX_nombre_modulo
cd python/modulos/XX_nombre_modulo
```

### Paso 2: Estructura Requerida

```
XX_nombre_modulo/
├── README.md                # Teoría (concepto, para qué, historia)
├── examples/
│   ├── 01_basico.py        # Ejemplo simple
│   ├── 02_intermedio.py    # Con más features
│   └── 03_avanzado.py      # Caso real
├── exercises/
│   ├── ejercicio_01.py     # Guiado
│   ├── ejercicio_02.py     # Intermedio
│   └── ejercicio_03.py     # Desafío
└── solutions/
    ├── ejercicio_01.py
    ├── ejercicio_02.py
    └── ejercicio_03.py
```

### Paso 3: Crear README.md

```markdown
# [TITULO]

Explicación clara del concepto.

## 🎯 Concepto

¿Qué es [tema]? En 1 párrafo.

## 💡 Para Qué Sirve

Casos de uso reales.

## 📚 Historia

¿Por qué se creó? ¿Alternativas históricas?

## 🧪 Ejemplos

Ver carpeta examples/

## 📝 Ejercicios

Ver carpeta exercises/
```

### Paso 4: Crear Ejemplos

Cada ejemplo:
- ✅ Funciona sin errores
- ✅ Tiene comentarios explicativos
- ✅ Toma < 30 segundos ejecutar
- ✅ Imprime resultados claros

```python
"""
Ejemplo: [Nombre descriptivo]

Qué aprenderás:
- Concepto A
- Concepto B
"""

def main():
    # Paso 1: Setup
    # Paso 2: Lógica
    # Paso 3: Output
    print("✅ Resultado")

if __name__ == "__main__":
    main()
```

### Paso 5: Crear Ejercicios

```python
"""
Ejercicio: [Nombre]

Dificultad: 🟢 Básica / 🟡 Intermedia / 🔴 Avanzada

Enunciado:
[Descripción clara de qué hacer]

Ayuda:
[Pistas si es necesario]

Verificación:
[Cómo saber si está correcto]
"""

def ejercicio():
    # Tu código aquí
    pass

if __name__ == "__main__":
    resultado = ejercicio()
    assert resultado == expected, "Verifica tu respuesta"
    print("✅ Correcto!")
```

### Paso 6: Agregar a Nextra

Crear archivo en `pages/[seccion]/XX-nombre.mdx`:

```mdx
# [Nombre del Módulo]

Descripción breve del tema.

## 📚 Contenido

- Concepto
- Ejemplos
- Ejercicios

## 🧪 Código

```bash
python python/modulos/XX_nombre/examples/01_basico.py
```

## 📖 Próximo Paso

[Link a siguiente módulo]
```

---

## ✅ Checklist: Antes de hacer PR

- [ ] Módulo tiene README.md
- [ ] 3+ ejemplos funcionales
- [ ] 3+ ejercicios con soluciones
- [ ] Página .mdx creada
- [ ] Todos los ejemplos corren sin errores
- [ ] Código está comentado
- [ ] Seguir estructura de carpetas
- [ ] Sin magic numbers (usar constantes)
- [ ] Tests pasan: `pytest python/modulos/XX/ -v`

---

## 🧪 Para la Sección Validation

### Agregar Nuevo Test

```python
# python/validation/test_XX.py

import pytest
from mock_llm import MockAnthropic

class TestMyFeature:
    def test_case_1(self):
        """
        Test: Descripción clara
        """
        # Setup
        mock = MockAnthropic()

        # Action
        result = mock.create_message(...)

        # Assert
        assert result is not None

# Ejecutar: pytest python/validation/test_XX.py -v
```

### Agregar Nuevo Ejemplo

```python
# python/validation/examples/XX_descripcion.py

"""
Ejemplo: [Descripción]

Cómo usar [concepto]
"""

def main():
    print("Ejecutando ejemplo...")
    # Código
    print("✅ Done!")

if __name__ == "__main__":
    main()

# Ejecutar: python python/validation/examples/XX_descripcion.py
```

---

## 📝 Reglas de Código

### Python

```python
# ✅ BUENO
def validar_respuesta_json(response: str) -> bool:
    """Valida que respuesta es JSON válido."""
    try:
        json.loads(response)
        return True
    except json.JSONDecodeError:
        return False

# ❌ MALO
def f(r):
    try:
        json.loads(r)
        return True
    except:
        return False
```

**Reglas:**
- Type hints siempre
- Docstrings en funciones
- Nombres descriptivos
- Comentarios solo si necesario
- Max 100 caracteres línea

### Markdown

```markdown
# Título
Explicación clara.

## Subsección
Más detalles.

### Sub-subsección
Muy específico.

> Cita o nota importante
```

---

## 🔄 Workflow: Hacer un PR

1. Fork el repo (si no tienes acceso)
2. Crea una rama: `git checkout -b feature/modulo-nuevo`
3. Agrega tu módulo siguiendo checklist
4. Testa todo: `pytest python/ -v`
5. Commit: `git commit -m "Add Modulo XX: [Descripción]"`
6. Push: `git push origin feature/modulo-nuevo`
7. Abre PR con descripción clara

---

## 📞 Preguntas?

- README no claro → Abre un issue
- Ejemplo no funciona → Abre un issue
- Sugerencia de nuevo módulo → Discusión

---

## ✨ Gracias por Contribuir

Este hub existe porque gente como tú quiere compartir conocimiento.

¡Agradecido! 🙏
