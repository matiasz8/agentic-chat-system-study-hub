# Link Validation

Este proyecto incluye validación automática de links en todos los archivos markdown antes de hacer commit.

## Cómo funciona

### Pre-commit Hook

Cuando ejecutas `git commit`, se ejecuta automáticamente:

1. **scripts/validate-links.sh** - Revisa todos los links internos
2. Si hay links rotos, el commit se bloquea
3. Se muestran los links problemáticos para que los corrijas

### Validación manual

Para validar links sin hacer commit:

```bash
./scripts/validate-links.sh
```

### Saltar la validación (solo si es urgente)

```bash
git commit --no-verify
```

## Scripts incluidos

- **scripts/validate-links.sh** - Valida todos los links internos
- **scripts/fix-links.sh** - (Futuro) Intenta corregir links automáticamente

## Links internos válidos

- Archivos: `[Título](/ruta/archivo)`
- Carpetas: `[Título](/ruta/carpeta)` → busca `carpeta/index.mdx`
- Fragmentos: `[Título](/ruta/archivo#fragmento)`

### Estructura esperada

El validador busca archivos en este orden:
1. `/ruta/archivo.mdx`
2. `/ruta/archivo.md`
3. `/ruta/archivo/index.mdx`
4. `/ruta/archivo/index.md`

## Ejemplo

```markdown
# Documentación

Revisa los [Fundamentos](/01-fundamentos) para entender mejor.

O ve directo a [Las 4 Capas](/01-fundamentos/02-4-capas).
```

## Notas

- Solo valida links internos (ignora http://, https://, mailto:, etc)
- Ignora fragmentos (#) para verificación de archivo (pero sí requiere que el archivo exista)
- Usa rutas absolutas desde `/pages/`
