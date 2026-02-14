# Guía de Contribución - Curso Android PMDM

## 🎯 Objetivo

Este documento describe cómo contribuir al repositorio del curso, ya sea para entregar ejercicios o colaborar con mejoras.

---

## 📋 Flujo de trabajo Git

### 1. Fork y Clone

```bash
# Fork desde GitHub (botón en la web)

# Clonar tu fork
git clone https://github.com/TU_USUARIO/curso-android-pmdm.git
cd curso-android-pmdm

# Añadir el repo original como upstream
git remote add upstream https://github.com/PROFESOR/curso-android-pmdm.git
```

### 2. Crear rama

```bash
# Actualizar main
git checkout main
git pull upstream main

# Crear rama para tu trabajo
git checkout -b feature/nombre-descriptivo

# Ejemplos de nombres:
# feature/ejercicio-03-listas
# fix/bug-navegacion
# docs/readme-actualizado
```

### 3. Hacer cambios y commits

```bash
# Añadir cambios
git add .

# Commit con mensaje descriptivo
git commit -m "feat: implementar lista de tareas con LazyColumn"

# Push a tu fork
git push origin feature/nombre-descriptivo
```

### 4. Crear Pull Request

1. Ve a tu fork en GitHub
2. Click en "Compare & pull request"
3. Rellena la plantilla del PR
4. Espera revisión del profesor

---

## 📝 Convención de commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>: <descripción breve>

[cuerpo opcional]
```

### Tipos

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Solo documentación |
| `style` | Formato (no afecta código) |
| `refactor` | Refactorización |
| `test` | Añadir/modificar tests |
| `chore` | Tareas de mantenimiento |

### Ejemplos

```bash
git commit -m "feat: añadir pantalla de detalle de tarea"
git commit -m "fix: corregir crash al rotar pantalla"
git commit -m "docs: actualizar README con instrucciones de instalación"
git commit -m "test: añadir tests para TodoViewModel"
git commit -m "refactor: extraer componentes reutilizables"
```

---

## 🔍 Antes de hacer PR

### Checklist

- [ ] El código compila: `./gradlew assembleDebug`
- [ ] Lint sin errores críticos: `./gradlew lint`
- [ ] Tests pasan: `./gradlew test`
- [ ] He probado en emulador/dispositivo
- [ ] Commits con mensajes descriptivos
- [ ] PR con descripción clara

### Ejecutar verificaciones

```bash
# Script completo de verificación
./scripts/check.sh

# O manualmente:
./gradlew assembleDebug
./gradlew lint
./gradlew test
```

---

## 🏗️ Estructura del código

### Arquitectura MVVM

```
app/src/main/java/com/example/app/
├── data/
│   ├── local/          # Room (Database, DAO, Entity)
│   ├── remote/         # Retrofit (API, DTO)
│   └── repository/     # Repositories
├── domain/
│   └── model/          # Modelos de dominio
├── ui/
│   ├── navigation/     # NavGraph
│   ├── screens/        # Pantallas (Screen, ViewModel, UiState)
│   ├── components/     # Composables reutilizables
│   └── theme/          # Material Theme
└── util/               # Utilidades
```

### Convenciones de código

- **Nombres de clases:** PascalCase (`TodoViewModel`, `UserRepository`)
- **Nombres de funciones:** camelCase (`loadUsers`, `onButtonClick`)
- **Nombres de constantes:** SCREAMING_SNAKE_CASE (`MAX_ITEMS`, `BASE_URL`)
- **Composables:** PascalCase con `@Composable` annotation

---

## 🐛 Reportar bugs

1. Verifica que no existe ya un issue similar
2. Crea un nuevo issue usando la plantilla "Bug Report"
3. Incluye:
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Versión de Android Studio
   - Logs de error

---

## ❓ Preguntas

- Usa la plantilla "Pregunta" para dudas sobre el curso
- Incluye contexto: lección, ejercicio, qué has intentado
- Revisa primero la documentación y issues existentes

---

## 📚 Recursos adicionales

- [Documentación de Kotlin](https://kotlinlang.org/docs/home.html)
- [Jetpack Compose](https://developer.android.com/jetpack/compose)
- [Android Architecture Components](https://developer.android.com/topic/libraries/architecture)
- [Material 3 Design](https://m3.material.io/)

---

¡Gracias por contribuir! 🎉
