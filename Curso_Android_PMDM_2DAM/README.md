# Curso Android PMDM - 2º DAM

> **Programación Multimedia y Dispositivos Móviles**  
> Kotlin + Jetpack Compose + Material 3 + MVVM + Room + Retrofit

---

## 📋 Índice

1. [Requisitos previos](#requisitos-previos)
2. [Instalación rápida](#instalación-rápida)
3. [Estructura del curso](#estructura-del-curso)
4. [Cómo seguir las lecciones](#cómo-seguir-las-lecciones)
5. [Proyectos evaluables](#proyectos-evaluables)
6. [Cómo entregar](#cómo-entregar)
7. [Evaluación y CI](#evaluación-y-ci)
8. [Soluciones](#soluciones)
9. [Soporte](#soporte)
10. [Guía de clase (2h)](#guía-de-clase-2h)

---

## Requisitos previos

- **Git** instalado y configurado
- **Cuenta de GitHub** con acceso al repositorio
- **8 GB RAM mínimo** (16 GB recomendado)
- **15 GB de espacio libre** en disco
- Windows 10/11, macOS 10.14+ o Linux

---

## Instalación rápida

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO/cursos/Curso_Android_PMDM_2DAM
```

### 2. Instalar Android Studio

Sigue la guía detallada en [docs/01-instalacion-android-studio.md](docs/01-instalacion-android-studio.md).

**Resumen:**
1. Descarga [Android Studio](https://developer.android.com/studio) (versión estable)
2. Instala con las opciones por defecto
3. En el primer arranque: instala SDK 34 y acepta licencias
4. Configura un emulador (Pixel 7, API 34)

### 3. Abrir un proyecto

Cada proyecto se abre **por separado**:

```
projects/
  todo-compose/starter/   ← Abre ESTA carpeta en Android Studio
  posts-offline/starter/  ← Abre ESTA carpeta en Android Studio
```

**Pasos:**
1. File → Open
2. Navega hasta la carpeta `starter/` del proyecto
3. Espera a que termine el Gradle Sync
4. Run → Run 'app'

---

## Estructura del curso

```
Curso_Android_PMDM_2DAM/
├── README.md                 ← Estás aquí
├── docs/                     ← Documentación general
│   ├── 00-introduccion.md
│   ├── 01-instalacion-android-studio.md
│   ├── 02-flujo-trabajo-git-y-entregas.md
│   ├── 03-guia-evaluacion.md
│   └── 04-solucion-problemas.md
├── syllabus/
│   ├── temario.md
│   └── calendario-sugerido-12-semanas.md
├── lessons/                  ← 12 lecciones teórico-prácticas
│   ├── 01-setup-y-gradle/
│   ├── 02-kotlin-essentials/
│   ├── 03-compose-basics/
│   ├── ...
│   └── 12-entrega-y-apk/
├── projects/                 ← Proyectos evaluables
│   ├── todo-compose/
│   │   ├── enunciado.md
│   │   ├── rubric.md
│   │   └── starter/          ← Proyecto Android completo
│   └── posts-offline/
│       ├── enunciado.md
│       ├── rubric.md
│       └── starter/          ← Proyecto Android completo
├── templates/
│   ├── PR_CHECKLIST.md
│   └── Rúbrica_base.md
└── scripts/
    └── check.sh
```

---

## Cómo seguir las lecciones

### Orden recomendado

1. **Semanas 1-2:** Lecciones 01-02 (setup, Kotlin)
2. **Semanas 3-4:** Lecciones 03-04 (Compose, MVVM)
3. **Semanas 5-6:** Lecciones 05-06 (navegación, listas) + **Proyecto 1**
4. **Semanas 7-8:** Lecciones 07-08 (API, coroutines)
5. **Semanas 9-10:** Lecciones 09-10 (Room, offline)
6. **Semanas 11-12:** Lecciones 11-12 (testing, APK) + **Proyecto 2**

### Cada lección incluye

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Teoría, pasos guiados, objetivos |
| `ejercicios.md` | Ejercicios con criterios de aceptación |
| `soluciones.md` | Explicación paso a paso de la solución |

### Metodología

1. Lee el `README.md` de la lección
2. Sigue los pasos guiados
3. Realiza los ejercicios
4. Consulta las soluciones **solo si te atascas**

---

## Proyectos evaluables

### Proyecto 1: Todo Compose (30% nota final)

**Entrega:** Semana 6

| Concepto | Descripción |
|----------|-------------|
| Tema | App de tareas con Room |
| Pantallas | Mínimo 2 (lista + detalle/crear) |
| Funcionalidades | CRUD, filtro, validaciones |
| Tests | Mínimo 3 tests de ViewModel |

📄 [Ver enunciado](projects/todo-compose/enunciado.md) | [Ver rúbrica](projects/todo-compose/rubric.md)

### Proyecto 2: App API + Offline (40% nota final)

**Entrega:** Semana 12

| Concepto | Descripción |
|----------|-------------|
| Tema | App con API REST y cache offline |
| Pantallas | Lista + detalle |
| Funcionalidades | Búsqueda, cache Room, manejo errores |
| Tests | Mínimo 5 tests de ViewModel |

📄 [Ver enunciado](projects/posts-offline/enunciado.md) | [Ver rúbrica](projects/posts-offline/rubric.md)

### Lecciones y participación (30% nota final)

- Ejercicios entregados a tiempo
- Calidad del código
- Participación en clase

---

## Cómo entregar

### Flujo de trabajo Git

```bash
# 1. Crea tu rama de entrega
git checkout -b entrega/proyecto-1-tu-nombre

# 2. Trabaja en la carpeta starter/
cd projects/todo-compose/starter

# 3. Haz commits frecuentes
git add .
git commit -m "feat: añadir pantalla de lista de tareas"

# 4. Push y abre PR
git push origin entrega/proyecto-1-tu-nombre
```

### Pull Request

1. Abre un PR hacia `main` (o la rama que indique el profesor)
2. Usa el template de PR incluido
3. Espera a que pasen los checks de CI
4. El profesor revisará y dará feedback

📄 Ver [docs/02-flujo-trabajo-git-y-entregas.md](docs/02-flujo-trabajo-git-y-entregas.md)

---

## Guía de clase (2h)

Guion paso a paso para impartir una clase completa (≈120 min) con el proyecto **Todo Compose**:

- `docs/05-guia-clase-2h-todo-compose.md`

---

## Evaluación y CI

### Checks automáticos (GitHub Actions)

Cada PR ejecuta automáticamente:

| Check | Descripción |
|-------|-------------|
| `./gradlew test` | Tests unitarios |
| `./gradlew lint` | Análisis estático |
| `./gradlew assembleDebug` | Compilación APK |

✅ **Todos los checks deben pasar** para que la entrega sea válida.

### Artifacts

El CI genera automáticamente el APK de debug como artifact descargable. El profesor puede descargar y probar sin instalar Android Studio.

---

## Soluciones

Las soluciones están disponibles en `soluciones.md` de cada lección y proyecto.

**Formato de soluciones:**
- Explicación paso a paso
- Código completo comentado
- Errores comunes y cómo evitarlos

> ⚠️ **Importante:** Intenta resolver por tu cuenta antes de consultar las soluciones. El aprendizaje real viene de equivocarse y corregir.

---

## Soporte

### Documentación de ayuda

- [Solución de problemas](docs/04-solucion-problemas.md)
- [Guía de evaluación](docs/03-guia-evaluacion.md)

### Recursos externos (complementarios)

- [Documentación oficial Android](https://developer.android.com/docs)
- [Jetpack Compose](https://developer.android.com/jetpack/compose)
- [Kotlin Docs](https://kotlinlang.org/docs/home.html)

### Contacto

- Abre un Issue en el repositorio con la etiqueta `pregunta`
- Consulta en clase o tutorías

---

## Stack tecnológico

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Kotlin | 1.9.x | Lenguaje |
| Jetpack Compose | 1.5.x | UI declarativa |
| Material 3 | 1.2.x | Diseño |
| ViewModel | 2.7.x | MVVM |
| Room | 2.6.x | Base de datos local |
| Retrofit | 2.9.x | Llamadas API |
| Coroutines | 1.7.x | Asincronía |
| Navigation Compose | 2.7.x | Navegación |
| JUnit | 4.13.x | Tests |

---

**¡Bienvenido al desarrollo Android!** 🚀
