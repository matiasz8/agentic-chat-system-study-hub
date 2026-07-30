# Build Validation System

## Overview
Sistema de validación de build que bloquea commits si hay problemas de integridad. Se ejecuta automáticamente antes de cada commit vía git hooks.

## Validaciones

El sistema realiza **8 validaciones automáticas**:

1. **Sintaxis MDX** - Detecta dobles llaves `{{{{` inválidas
2. **Componentes JSX** - Verifica que RouteProgress tenga `export default`
3. **Imports** - Confirma que los imports estén presentes
4. **_meta.json files** - Valida que existan archivos de navegación
5. **Integridad de archivos** - Verifica que los archivos cierren correctamente
6. **Paréntesis balanceados** - Cuenta `(` vs `)`
7. **Llaves balanceadas** - Cuenta `{` vs `}`
8. **console.log** - Alerta sobre debug statements (no bloquea)

## Ejecución

### Local (Pre-commit Hook)
```bash
# Se ejecuta automáticamente antes de cada commit
git commit -m "mensaje"

# Saltar validación (solo en emergencias)
git commit --no-verify
```

### Manual
```bash
# Solo validar links
./scripts/validate-links.sh

# Solo validar build
./scripts/check-build.sh

# Ambos
./.git/hooks/pre-commit
```

## Archivos

- `.git/hooks/pre-commit` - Hook que ejecuta validaciones
- `scripts/validate-links.sh` - Valida links internos
- `scripts/check-build.sh` - Valida integridad del build

## GitHub Actions

El workflow `.github/workflows/validate.yml` ejecuta:
- `npm ci` - Install dependencias
- `npm run lint` - Linting (si existe)
- `npm run build` - Build
- `python3 -m compileall python/modulos/` - Valida Python

## Flujo de Commits

```
user: git commit -m "..."
  ↓
.git/hooks/pre-commit
  ├─ ./scripts/validate-links.sh (validar links)
  ├─ ./scripts/check-build.sh (validar build)
  └─ exit 0 (OK) o exit 1 (BLOQUEADO)
  ↓
Si pasa: commit se crea
Si falla: commit bloqueado, mostrar errores
```

## Troubleshooting

### Error: "Paréntesis desbalanceados"
```
❌ BUILD CHECK FALLÓ: Paréntesis desbalanceados
```
**Solución**: Revisar componentes JSX, especialmente funciones y condicionales

### Error: "Llaves desbalanceadas"
```
❌ BUILD CHECK FALLÓ: Llaves desbalanceadas
```
**Solución**: Revisar styled-jsx blocks `<style jsx>` o objetos JavaScript

### Error: "Links rotos"
```
⚠️ COMMIT BLOQUEADO: Hay links rotos
```
**Solución**: Ejecutar `./scripts/validate-links.sh` para ver cuáles links están rotos

### Bypass en emergencia
```bash
git commit --no-verify
```
⚠️ **Usar solo en emergencias** - el build aún fallará en GitHub Actions

## Monitoreo

Verificar status del último build:
```bash
gh run list --workflow validate.yml
```

Ver detalles de un run:
```bash
gh run view RUN_ID --log
```

## Referencias

- Link validation: `docs/LINK_VALIDATION.md`
- Status del proyecto: `docs/PROJECT_STATUS.md`
