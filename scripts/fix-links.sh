#!/bin/bash

echo "🔧 Corrigiendo links rotos..."

# Mapeo de rutas viejas a nuevas
declare -A LINK_MAP=(
    # Rutas antiguas de learning paths
    ["/rutas/estudio"]="/04-rutas/estudio"
    ["/rutas/poc"]="/04-rutas/poc"
    ["/rutas/produccion"]="/04-rutas/produccion"
    ["/rutas/learning-paths"]="/04-rutas"
    ["/rutas/module-map"]="/04-rutas"
    
    # Frontend
    ["/frontend/00-vercel-intro"]="/02-arquitectura/frontend/00-vercel-intro"
    ["/frontend/01-streaming"]="/02-arquitectura/frontend/01-streaming"
    ["/frontend/02-generative-ui"]="/02-arquitectura/frontend/02-generative-ui"
    ["/frontend/03-frontend-completo"]="/02-arquitectura/frontend/03-frontend-completo"
    
    # Orchestration
    ["/orchestration/10-fundamentos-grafos"]="/02-arquitectura/orchestration/10-fundamentos-grafos"
    ["/orchestration/11-state"]="/02-arquitectura/orchestration/11-state"
    ["/orchestration/12-nodos"]="/02-arquitectura/orchestration/12-nodos"
    ["/orchestration/13-aristas"]="/02-arquitectura/orchestration/13-aristas"
    ["/orchestration/14-checkpoints"]="/02-arquitectura/orchestration/14-checkpoints"
    
    # Runtime
    ["/runtime/20-serverless-basics"]="/02-arquitectura/runtime/20-serverless-basics"
    ["/runtime/21-identity-forwarding"]="/02-arquitectura/runtime/21-identity-forwarding"
    ["/runtime/22-agentcore-governance"]="/02-arquitectura/runtime/22-agentcore-governance"
    ["/runtime/23-cedar-policies"]="/02-arquitectura/runtime/23-cedar-policies"
    ["/runtime/24-tools-management"]="/02-arquitectura/runtime/24-tools-management"
    
    # Validation
    ["/validacion/00-testing-basico"]="/03-validacion/00-testing-basico"
    ["/validacion/01-testing-prompts"]="/03-validacion/01-testing-prompts"
    ["/validacion/02-validation-workflows"]="/03-validacion/02-validation-workflows"
    ["/validacion/03-e2e-testing"]="/03-validacion/03-e2e-testing"
    ["/validacion/04-ci-cd"]="/03-validacion/04-ci-cd"
    
    # Fundamentos
    ["/fundamentos/4-capas"]="/01-fundamentos/02-4-capas"
    
    # Ask Sage
    ["/ask-sage/00-introduccion"]="/ask-sage/00-introduccion"
)

# Iterar sobre todos los archivos .mdx y .md
FIXED=0
find pages -name "*.mdx" -o -name "*.md" | while read file; do
    CONTENT=$(cat "$file")
    MODIFIED=false
    
    for OLD_LINK in "${!LINK_MAP[@]}"; do
        NEW_LINK="${LINK_MAP[$OLD_LINK]}"
        
        # Reemplazar en todos los formatos de links
        if echo "$CONTENT" | grep -q "$OLD_LINK"; then
            # [text](/old) → [text](/new)
            sed -i "s|\]($OLD_LINK)|\]($NEW_LINK)|g" "$file"
            # [text](/old#anchor) → [text](/new#anchor)
            sed -i "s|\]($OLD_LINK#|\]($NEW_LINK#|g" "$file"
            MODIFIED=true
            ((FIXED++))
        fi
    done
    
    if [ "$MODIFIED" = true ]; then
        echo "  ✓ $file"
    fi
done

echo ""
echo "✅ Se corrigieron aproximadamente $FIXED referencias"
