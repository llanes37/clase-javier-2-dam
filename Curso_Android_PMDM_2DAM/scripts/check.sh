#!/bin/bash
# check.sh - Script de verificación para proyectos Android
# Uso: ./scripts/check.sh [ruta-al-proyecto]

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo ""
    echo "=========================================="
    echo "$1"
    echo "=========================================="
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Directorio del proyecto
PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"

echo "🔍 Verificando proyecto Android en: $(pwd)"

# Verificar que es un proyecto Android
if [ ! -f "build.gradle.kts" ] && [ ! -f "build.gradle" ]; then
    print_error "No se encontró build.gradle. ¿Es este un proyecto Android?"
    exit 1
fi

print_header "1. VERIFICANDO ESTRUCTURA"

# Verificar archivos esenciales
REQUIRED_FILES=(
    "app/build.gradle.kts"
    "app/src/main/AndroidManifest.xml"
    "settings.gradle.kts"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "Encontrado: $file"
    else
        # Probar con extensión .gradle en lugar de .kts
        alt_file="${file/.kts/}"
        if [ -f "$alt_file" ]; then
            print_success "Encontrado: $alt_file"
        else
            print_error "Falta: $file"
        fi
    fi
done

print_header "2. COMPILANDO PROYECTO"

# Dar permisos al gradlew
if [ -f "gradlew" ]; then
    chmod +x gradlew
    
    echo "Ejecutando: ./gradlew assembleDebug..."
    if ./gradlew assembleDebug --quiet; then
        print_success "Compilación exitosa"
    else
        print_error "Error de compilación"
        exit 1
    fi
else
    print_warning "No se encontró gradlew, saltando compilación"
fi

print_header "3. EJECUTANDO LINT"

if [ -f "gradlew" ]; then
    echo "Ejecutando: ./gradlew lint..."
    if ./gradlew lint --quiet 2>/dev/null; then
        print_success "Lint completado"
        
        # Verificar si hay errores en el reporte
        LINT_REPORT="app/build/reports/lint-results-debug.html"
        if [ -f "$LINT_REPORT" ]; then
            echo "   Reporte disponible en: $LINT_REPORT"
        fi
    else
        print_warning "Lint completó con advertencias"
    fi
fi

print_header "4. EJECUTANDO TESTS"

if [ -f "gradlew" ]; then
    echo "Ejecutando: ./gradlew test..."
    if ./gradlew test --quiet 2>/dev/null; then
        print_success "Tests pasaron"
    else
        print_warning "Algunos tests fallaron"
    fi
fi

print_header "5. VERIFICANDO ARQUITECTURA"

# Verificar estructura de carpetas común
ARCH_FOLDERS=(
    "app/src/main/java"
    "app/src/test/java"
)

for folder in "${ARCH_FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        print_success "Carpeta: $folder"
    else
        print_warning "Falta carpeta: $folder"
    fi
done

# Buscar patrones de arquitectura
echo ""
echo "Buscando patrones de arquitectura..."

if grep -rq "ViewModel" app/src/main/java 2>/dev/null; then
    print_success "Encontrado: ViewModel"
else
    print_warning "No se encontró ViewModel"
fi

if grep -rq "Repository" app/src/main/java 2>/dev/null; then
    print_success "Encontrado: Repository"
else
    print_warning "No se encontró Repository"
fi

if grep -rq "StateFlow\|MutableStateFlow" app/src/main/java 2>/dev/null; then
    print_success "Encontrado: StateFlow"
else
    print_warning "No se encontró StateFlow"
fi

if grep -rq "@Composable" app/src/main/java 2>/dev/null; then
    print_success "Encontrado: Jetpack Compose"
else
    print_warning "No se encontró Jetpack Compose"
fi

if grep -rq "@Entity\|@Dao" app/src/main/java 2>/dev/null; then
    print_success "Encontrado: Room Database"
else
    print_warning "No se encontró Room"
fi

print_header "6. VERIFICANDO GIT"

if [ -d ".git" ]; then
    print_success "Repositorio Git encontrado"
    
    # Contar commits
    COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    echo "   Commits: $COMMIT_COUNT"
    
    # Verificar si hay cambios sin commitear
    if git diff --quiet && git diff --staged --quiet; then
        print_success "Working directory limpio"
    else
        print_warning "Hay cambios sin commitear"
    fi
else
    print_warning "No es un repositorio Git"
fi

print_header "RESUMEN"

echo ""
echo "Verificación completada."
echo ""
echo "Próximos pasos:"
echo "  1. Revisar warnings y errores arriba"
echo "  2. Ejecutar la app en emulador para pruebas manuales"
echo "  3. Crear PR si todo está correcto"
echo ""
