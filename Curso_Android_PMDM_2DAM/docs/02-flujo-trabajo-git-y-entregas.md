# Flujo de trabajo Git y entregas

## Resumen del flujo

```
main (protegida)
  │
  └── entrega/proyecto-1-tu-nombre
        │
        ├── commit: feat: pantalla lista
        ├── commit: feat: pantalla detalle
        ├── commit: fix: validación formulario
        └── commit: test: tests viewmodel
              │
              └── Pull Request → main
                    │
                    ├── CI: ✅ tests
                    ├── CI: ✅ lint
                    ├── CI: ✅ build
                    └── Review del profesor
```

---

## Configuración inicial (solo una vez)

### 1. Clonar el repositorio

```bash
git clone https://github.com/ORGANIZACION/REPO.git
cd REPO
```

### 2. Configurar tu identidad

```bash
git config user.name "Tu Nombre"
git config user.email "tu@email.com"
```

### 3. Verificar configuración

```bash
git config --list
```

---

## Flujo para cada entrega

### Paso 1: Actualizar main

Antes de empezar cualquier trabajo:

```bash
git checkout main
git pull origin main
```

### Paso 2: Crear rama de entrega

**Nomenclatura obligatoria:**

```
entrega/proyecto-N-nombre-apellido
```

**Ejemplos:**
```bash
git checkout -b entrega/proyecto-1-juan-garcia
git checkout -b entrega/proyecto-2-maria-lopez
```

### Paso 3: Trabajar en tu código

Navega a la carpeta del proyecto:

```bash
cd cursos/Curso_Android_PMDM_2DAM/projects/todo-compose/starter
```

Abre esta carpeta en Android Studio y trabaja normalmente.

### Paso 4: Hacer commits frecuentes

**Formato de commits (Conventional Commits):**

```
tipo: descripción breve

Tipos:
- feat: nueva funcionalidad
- fix: corrección de bug
- docs: documentación
- style: formato (no cambia lógica)
- refactor: reestructuración sin cambiar funcionalidad
- test: añadir o modificar tests
- chore: tareas de mantenimiento
```

**Ejemplos:**

```bash
git add .
git commit -m "feat: implementar pantalla de lista de tareas"

git add .
git commit -m "feat: añadir Room database y entities"

git add .
git commit -m "fix: corregir validación de campos vacíos"

git add .
git commit -m "test: añadir tests para TaskViewModel"
```

**Buenas prácticas:**
- Commits pequeños y frecuentes
- Un commit por funcionalidad/fix
- Mensaje claro y en imperativo
- No commits tipo "cambios", "arreglos", "wip"

### Paso 5: Push a tu rama

```bash
git push origin entrega/proyecto-1-tu-nombre
```

Si es el primer push de la rama:

```bash
git push -u origin entrega/proyecto-1-tu-nombre
```

### Paso 6: Crear Pull Request

1. Ve a GitHub → Tu repositorio
2. Verás un banner: "entrega/proyecto-1-... had recent pushes"
3. Clic en **Compare & pull request**
4. Rellena el formulario:
   - **Title:** `Entrega Proyecto 1 - Tu Nombre`
   - **Description:** Usa el template (se carga automáticamente)
5. Revisa que la PR va de tu rama → `main`
6. Clic en **Create pull request**

### Paso 7: Esperar CI

El sistema ejecutará automáticamente:

```
✓ ./gradlew test      → Tests pasan
✓ ./gradlew lint      → Sin errores de lint
✓ ./gradlew assembleDebug → APK generado
```

**Si algún check falla:**
1. Lee el log del error en GitHub Actions
2. Corrige en local
3. Haz commit y push
4. Los checks se re-ejecutan automáticamente

### Paso 8: Review del profesor

- El profesor revisará tu PR
- Puede dejar comentarios o pedir cambios
- Si pide cambios: corrige, commit, push
- Cuando apruebe: el profesor hará merge

---

## Comandos útiles

### Ver estado

```bash
git status          # Archivos modificados
git log --oneline   # Historial de commits
git branch -a       # Todas las ramas
```

### Deshacer cambios

```bash
# Descartar cambios en un archivo (no commiteado)
git checkout -- archivo.kt

# Descartar todos los cambios no commiteados
git checkout -- .

# Deshacer último commit (mantiene cambios)
git reset --soft HEAD~1

# Deshacer último commit (descarta cambios) ⚠️ CUIDADO
git reset --hard HEAD~1
```

### Sincronizar con main

Si main ha avanzado mientras trabajas:

```bash
git checkout main
git pull origin main
git checkout entrega/proyecto-1-tu-nombre
git merge main
# Resuelve conflictos si los hay
git push
```

---

## Estructura de la PR

### Título

```
Entrega Proyecto N - Nombre Apellido
```

### Descripción (template)

El repositorio incluye un template automático. Asegúrate de completar:

- [ ] Checklist de funcionalidades
- [ ] Descripción de lo implementado
- [ ] Capturas de pantalla (opcional pero recomendado)
- [ ] Notas para el revisor

---

## Errores comunes

### "Permission denied"

No tienes permisos de push. Contacta al profesor.

### "Merge conflict"

Hay conflictos con main. Resuélvelos:

```bash
git pull origin main
# Edita los archivos con conflictos
# Busca <<<<<<< y >>>>>>>
git add .
git commit -m "fix: resolver conflictos con main"
git push
```

### "CI failed"

1. Ve a la pestaña **Actions** en GitHub
2. Clic en el workflow fallido
3. Lee el log de errores
4. Corrige y haz push

### Olvidé hacer pull antes de empezar

```bash
git stash                    # Guarda tus cambios temporalmente
git pull origin main         # Actualiza
git stash pop                # Recupera tus cambios
# Resuelve conflictos si los hay
```

---

## Reglas importantes

1. **No hagas push directo a main** - Siempre via PR
2. **No modifiques archivos fuera de starter/** - Solo tu proyecto
3. **No borres archivos del enunciado** - Solo añade/modifica código
4. **Respeta la fecha límite** - PRs tardías penalizan
5. **Un PR por proyecto** - No mezcles proyectos

---

## Flujo visual

```
┌─────────────────────────────────────────────────────────┐
│                        GitHub                            │
├─────────────────────────────────────────────────────────┤
│  main (protegida)                                        │
│    │                                                     │
│    │  ┌─── Pull Request ◄──────────────────────┐        │
│    │  │                                         │        │
│    ▼  ▼                                         │        │
│  ────●────●────●────●────●────●                 │        │
│                              │                  │        │
│                              └──► CI checks     │        │
│                                   ✓ test        │        │
│                                   ✓ lint        │        │
│                                   ✓ build       │        │
│                                   ⬇ artifact    │        │
│                                      (APK)      │        │
│                                                 │        │
│  tu-rama                                        │        │
│    ●────●────●────●────●───────────────────────►┘        │
│    ▲                                                     │
│    │ push                                                │
└────┼────────────────────────────────────────────────────┘
     │
┌────┴────────────────────────────────────────────────────┐
│                      Tu PC local                         │
├─────────────────────────────────────────────────────────┤
│  git checkout -b entrega/proyecto-1-tu-nombre           │
│  # trabajar en Android Studio                            │
│  git add .                                               │
│  git commit -m "feat: ..."                              │
│  git push origin entrega/proyecto-1-tu-nombre           │
└─────────────────────────────────────────────────────────┘
```

---

## Siguiente paso

→ [03-guia-evaluacion.md](03-guia-evaluacion.md)
