#!/usr/bin/env python3
"""
Test de Configuración: Verifica que todo esté instalado correctamente.
Ejecuta: python test_setup.py
"""


def test_imports():
    """Intenta importar todas las librerías necesarias"""
    print("\n🧪 Verificando dependencias...\n")

    tests = {
        "langgraph": "pip install langgraph",
        "anthropic": "pip install anthropic",
        "pydantic": "pip install pydantic",
        "dotenv": "pip install python-dotenv",
    }

    all_good = True
    for lib, install_cmd in tests.items():
        try:
            __import__(lib.replace("-", "_"))
            print(f"✅ {lib:20} - OK")
        except ImportError:
            print(f"❌ {lib:20} - FALLO ({install_cmd})")
            all_good = False

    print()
    if all_good:
        print("✨ ¡Todas las dependencias están instaladas!")
        print("👉 Próximo paso: cd modulos/00_fundamentos_grafos/")
    else:
        print("⚠️  Algunas librerías faltan. Instálalas con:")
        print("   pip install -r requirements.txt")

    return all_good


if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)
