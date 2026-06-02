#!/bin/bash

# Build check script
# Verifica que los archivos estén listos para build

echo "🔨 Verificando integridad del build..."
echo ""

ERROR_COUNT=0

# 1. Verificar que no haya archivos MDX con sintaxis inválida
echo "1️⃣ Verificando sintaxis MDX..."
if grep -r "{{{{" pages/ --include="*.mdx" > /dev/null 2>&1; then
  echo "   ❌ Doble llave detectada en MDX ({{ es válido, pero no {{{{)"
  ERROR_COUNT=$((ERROR_COUNT + 1))
fi

# 2. Verificar que los componentes JSX estén bien formados
echo "2️⃣ Verificando componentes JSX..."
if ! grep -q "export default" components/RouteProgress.jsx; then
  echo "   ❌ RouteProgress no tiene export default"
  ERROR_COUNT=$((ERROR_COUNT + 1))
else
  echo "   ✅ RouteProgress.jsx exporta correctamente"
fi

# 3. Verificar que no haya imports rotos
echo "3️⃣ Verificando imports..."
if grep -q "import.*from '[^']*'" components/RouteProgress.jsx; then
  echo "   ✅ Imports presentes en RouteProgress"
fi

# 4. Verificar _meta.json files
echo "4️⃣ Verificando _meta.json files..."
meta_files=$(find pages -name "_meta.json" | wc -l)
if [ "$meta_files" -gt 0 ]; then
  echo "   ✅ Encontrados $meta_files archivos _meta.json"
fi

# 5. Verificar que no haya archivos truncados
echo "5️⃣ Verificando integridad de archivos..."
if [ -s components/RouteProgress.jsx ]; then
  last_line=$(tail -1 components/RouteProgress.jsx | tr -d ' ')
  if [ "$last_line" = "}" ]; then
    echo "   ✅ RouteProgress.jsx cierra correctamente"
  else
    echo "   ❌ RouteProgress.jsx no cierra bien"
    ERROR_COUNT=$((ERROR_COUNT + 1))
  fi
fi

# 6. Verificar paréntesis balanceados en JSX
echo "6️⃣ Verificando paréntesis balanceados..."
open_paren=$(grep -o "(" components/RouteProgress.jsx | wc -l)
close_paren=$(grep -o ")" components/RouteProgress.jsx | wc -l)
if [ "$open_paren" -eq "$close_paren" ]; then
  echo "   ✅ Paréntesis balanceados: $open_paren/$close_paren"
else
  echo "   ❌ Paréntesis desbalanceados: $open_paren != $close_paren"
  ERROR_COUNT=$((ERROR_COUNT + 1))
fi

# 7. Verificar llaves balanceadas
echo "7️⃣ Verificando llaves balanceadas..."
open_braces=$(grep -o "{" components/RouteProgress.jsx | wc -l)
close_braces=$(grep -o "}" components/RouteProgress.jsx | wc -l)
if [ "$open_braces" -eq "$close_braces" ]; then
  echo "   ✅ Llaves balanceadas: $open_braces/$close_braces"
else
  echo "   ❌ Llaves desbalanceadas: $open_braces != $close_braces"
  ERROR_COUNT=$((ERROR_COUNT + 1))
fi

# 8. Verificar que no haya consola.log en producción
echo "8️⃣ Verificando console.log..."
if grep -q "console.log" components/RouteProgress.jsx; then
  grep_count=$(grep "console.log" components/RouteProgress.jsx | wc -l)
  echo "   ⚠️  Encontrados $grep_count console.log (deberían estar solo en desarrollo)"
  # No es error crítico
fi

echo ""
echo "══════════════════════════════════════════════════"

if [ $ERROR_COUNT -eq 0 ]; then
  echo "✅ BUILD CHECK PASADO: Todo está listo para build"
  echo "══════════════════════════════════════════════════"
  exit 0
else
  echo "❌ BUILD CHECK FALLÓ: $ERROR_COUNT problemas encontrados"
  echo "══════════════════════════════════════════════════"
  exit 1
fi
