#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
TEMP_FILE=$(mktemp)

echo -e "${YELLOW}🔍 Validando links en archivos markdown...${NC}"
echo ""

# Buscar todos los archivos y sus links
find pages -name "*.mdx" -o -name "*.md" | while read file; do
    grep -o '\[.*\]([^)]*)'  "$file" 2>/dev/null | while read -r match; do
        link=$(echo "$match" | sed 's/.*(\([^)]*\)).*/\1/')
        
        # Solo validar links internos
        if [[ ! "$link" =~ ^(http|https|mailto|ftp|#|[a-z]+:) ]]; then
            path="${link%%#*}"
            
            if [[ -z "$path" ]] || [[ "$path" == "/" ]]; then
                continue
            fi
            
            if [[ "$path" == /* ]]; then
                resolved="pages${path%/}"
            else
                file_dir=$(dirname "$file")
                resolved="$file_dir/$path"
            fi
            
            resolved=$(echo "$resolved" | sed 's|/\.||g' | sed 's|/[^/]*/../||g')
            
            found=false
            if [[ -f "${resolved}.mdx" ]] || [[ -f "${resolved}.md" ]] || \
               [[ -f "${resolved}/index.mdx" ]] || [[ -f "${resolved}/index.md" ]]; then
                found=true
            fi
            
            if [[ "$found" == false ]]; then
                echo "$file|$link" >> "$TEMP_FILE"
            fi
        fi
    done
done

# Procesar resultados
if [ -f "$TEMP_FILE" ] && [ -s "$TEMP_FILE" ]; then
    while IFS='|' read -r file link; do
        echo -e "${RED}✗ ROTO${NC}: $file"
        echo -e "  Link: $link"
        echo ""
        ((ERRORS++))
    done < "$TEMP_FILE"
fi

rm -f "$TEMP_FILE"

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Todos los links son válidos${NC}"
    exit 0
else
    echo -e "${RED}❌ Se encontraron $ERRORS links rotos${NC}"
    exit 1
fi
