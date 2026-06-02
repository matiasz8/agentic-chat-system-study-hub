# 🔗 Link Validation Setup

Se ha instalado validación automática de links para el repositorio. Aquí está cómo funciona:

## ✅ Quick Start

```bash
# Validar links manualmente
./scripts/validate-links.sh

# Ver si hay links rotos
git status

# Hacer commit (validará automáticamente)
git commit -m "tu mensaje"

# Si necesitas saltarte la validación (no recomendado)
git commit --no-verify
```

## 📋 Componentes instalados

### 1. **scripts/validate-links.sh**
- Escanea todos los archivos `.mdx` y `.md`
- Busca links internos: `[texto](/ruta/archivo)`
- Verifica que existan los archivos o carpetas con `index.mdx`
- Retorna código 0 si todo está bien, 1 si hay problemas

### 2. **.git/hooks/pre-commit**
- Se ejecuta automáticamente antes de cada `git commit`
- Llama a `scripts/validate-links.sh`
- Bloquea el commit si hay links rotos
- Muestra qué links están rotos para que los corrijas

## 🎯 Cómo usar

### Validar sin hacer commit
```bash
./scripts/validate-links.sh
```

Salida:
```
🔍 Validando links en archivos markdown...

✗ ROTO: pages/archivo.mdx
  Link: /ruta/inexistente

❌ Se encontraron 1 links rotos
```

### Hacer un commit (con validación automática)
```bash
git add pages/nueva-pagina.mdx
git commit -m "docs: add new page"
```

Si hay links rotos:
```
🔗 Validando links antes de commit...
...
⚠️  COMMIT BLOQUEADO: Hay links rotos

Para solucionar:
1. Revisa los links listados arriba
2. Corrige o elimina los links rotos
3. Intenta commit de nuevo

O si necesitas saltarte esta validación:
  git commit --no-verify
```

## 🔧 Cómo escribir links correctamente

### Links válidos
```markdown
# Ruta absoluta desde /pages
[Fundamentos](/01-fundamentos)
[Cuatro Capas](/01-fundamentos/02-4-capas)

# Links con fragmentos
[Orchestration](/02-arquitectura/orchestration#state)

# Carpetas (busca automáticamente index.mdx)
[Rutas](/04-rutas)  # ← Busca 04-rutas/index.mdx
```

### Links inválidos (no se validan)
```markdown
[Google](https://google.com)  # Enlaces externos
[Email](mailto:test@test.com) # Correo
[Referencias](#fragmento)     # Solo fragmento
```

## 📊 Estructura de archivos esperada

El validador busca en este orden:

```
/ruta/archivo       → archivo.mdx
                    → archivo.md
                    → archivo/index.mdx
                    → archivo/index.md
```

Ejemplos:
- `/01-fundamentos` → busca `pages/01-fundamentos/index.mdx`
- `/01-fundamentos/02-4-capas` → busca `pages/01-fundamentos/02-4-capas.mdx`

## ⚙️ Configuración de Husky

Los hooks están configurados en:
- `.husky/pre-commit` - Definición del hook
- `.git/hooks/pre-commit` - Symlink/copia instalada

Si necesitas reinstalar:
```bash
cp .husky/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## 🚀 Ventajas

- ✅ Previene links rotos en documentación
- ✅ Validación automática, no manual
- ✅ Fallos claros con ubicación exacta
- ✅ Puedes saltarlo si realmente necesitas (`--no-verify`)
- ✅ Funciona offline, sin dependencias externas

## 📝 Notas

- El script usa bash puro (sin npm/node)
- Compatible con cualquier shell POSIX
- Rápido (~200ms para 80+ páginas)
- Ignora links externos y especiales automáticamente
