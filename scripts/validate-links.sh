#!/bin/bash

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

echo -e "${YELLOW}🔍 Validando links en archivos markdown...${NC}"
echo ""

# Buscar todos los archivos .mdx y .md
find pages -name "*.mdx" -o -name "*.md" | while read file; do
    # Usar grep para encontrar enlaces y grep -o para extractarlos
    # Patrón: [texto](/ruta) o [texto](ruta)
    grep -o '\[.*\]([^)]*)'  "$file" 2>/dev/null | while read -r match; do
        # Extraer solo la URL entre paréntesis
        link=$(echo "$match" | sed 's/.*(\([^)]*\)).*/\1/')
        
        # Solo validar links internos (sin protocolo http/https/mailto/etc)
        if [[ ! "$link" =~ ^(http|https|mailto|ftp|#|[a-z]+:) ]]; then
            
            # Extraer la ruta sin fragmentos
            path="${link%%#*}"
            
            # Ignorar links vacíos o solo /
            if [[ -z "$path" ]] || [[ "$path" == "/" ]]; then
                continue
            fi
            
            # Resolver la ruta absoluta
            if [[ "$path" == /* ]]; then
                # Ruta absoluta desde pages/
                resolved="pages${path%/}"
            else
                # Ruta relativa desde el directorio del archivo
                file_dir=$(dirname "$file")
                resolved="$file_dir/$path"
            fi
            
            # Normalizar (eliminar ../ y ./)
            resolved=$(echo "$resolved" | sed 's|/\.||g' | sed 's|/[^/]*/../||g')
            
            # Verificar si existe
            found=false
            if [[ -f "${resolved}.mdx" ]] || [[ -f "${resolved}.md" ]] || \
               [[ -f "${resolved}/index.mdx" ]] || [[ -f "${resolved}/index.md" ]]; then
                found=true
            fi
            
            if [[ "$found" == false ]]; then
                echo -e "${RED}✗ ROTO${NC}: $file"
                echo -e "  Link: $link"
                echo ""
                ((ERRORS++))
            fi
        fi
    done
done

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Todos los links son válidos${NC}"
    exit 0
else
    echo -e "${RED}❌ Se encontraron $ERRORS links rotos${NC}"
    exit 1
fi
