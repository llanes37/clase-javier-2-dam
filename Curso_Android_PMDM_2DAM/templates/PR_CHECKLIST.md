# Checklist de Pull Request - Android PMDM

## Antes de crear el PR

### Código
- [ ] El código compila sin errores (`./gradlew assembleDebug`)
- [ ] Lint no muestra errores críticos (`./gradlew lint`)
- [ ] Los tests pasan (`./gradlew test`)
- [ ] He probado la app en emulador/dispositivo
- [ ] He seguido la arquitectura MVVM

### Estilo
- [ ] Nombres de variables/funciones descriptivos en inglés
- [ ] Comentarios donde sea necesario (en español está bien)
- [ ] No hay código comentado ni prints de debug
- [ ] Imports organizados (sin wildcards `*`)

### Git
- [ ] He hecho commits atómicos con mensajes descriptivos
- [ ] Mi rama está actualizada con `main`
- [ ] He resuelto los conflictos (si los había)

### Documentación
- [ ] README actualizado si es necesario
- [ ] Funcionalidades nuevas documentadas

---

## Descripción del PR

### ¿Qué hace este PR?
<!-- Describe brevemente los cambios -->

### ¿Por qué es necesario?
<!-- Explica la motivación -->

### ¿Cómo probarlo?
<!-- Pasos para probar la funcionalidad -->

1. 
2. 
3. 

### Screenshots/Videos (si aplica)
<!-- Añade capturas de los cambios visuales -->

---

## Tipo de cambio

- [ ] 🐛 Bug fix
- [ ] ✨ Nueva funcionalidad
- [ ] 📝 Documentación
- [ ] 🎨 Estilo/UI
- [ ] ♻️ Refactoring
- [ ] 🧪 Tests

---

## Notas adicionales
<!-- Cualquier información extra para el revisor -->
