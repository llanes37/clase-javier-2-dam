# Ejercicios - Lección 12: Generar APK y distribución

## Ejercicio 1: Configurar build types

### Instrucciones

Configura tu proyecto con build types diferenciados.

### Requisitos

1. **Debug build:**
   - Application ID suffix: `.debug`
   - Version name suffix: `-debug`
   - Debuggable: true

2. **Release build:**
   - Minify enabled
   - Shrink resources enabled
   - ProGuard configurado

3. **Verificar** que ambas variantes compilan

### Criterios de aceptación

- [ ] Debug APK tiene ID diferente (puede instalarse junto a release)
- [ ] Release APK está ofuscado
- [ ] Ambas variantes funcionan correctamente

---

## Ejercicio 2: Crear y configurar keystore

### Instrucciones

Crea un keystore para firmar tu app.

### Pasos

1. Genera un keystore con keytool o Android Studio
2. Configura signing en build.gradle usando local.properties
3. Añade local.properties a .gitignore
4. Genera APK release firmado

### Criterios de aceptación

- [ ] Keystore creado
- [ ] Signing configurado (NO hardcodeado)
- [ ] local.properties en .gitignore
- [ ] APK release generado y firmado

---

## Ejercicio 3: ProGuard rules

### Instrucciones

Configura ProGuard para tu proyecto.

### Requisitos

Añade reglas para:
- Clases de modelo (data classes)
- Retrofit interfaces
- Room entities
- Cualquier librería que uses

### Verificación

1. Genera release APK
2. Ejecuta la app
3. Verifica que todas las funcionalidades funcionan
4. Guarda el mapping.txt

### Criterios de aceptación

- [ ] ProGuard rules configuradas
- [ ] App release funciona correctamente
- [ ] No hay crashes por ofuscación
- [ ] mapping.txt generado

---

## Ejercicio 4: Versionado

### Instrucciones

Implementa un sistema de versionado semántico.

### Requisitos

1. Configura versión inicial: 1.0.0 (versionCode 1)
2. Simula un bug fix: 1.0.1 (versionCode 2)
3. Simula nueva feature: 1.1.0 (versionCode 3)
4. Muestra la versión en la pantalla de "Acerca de"

### Código sugerido

```kotlin
// Para obtener la versión en runtime
val versionName = context.packageManager
    .getPackageInfo(context.packageName, 0).versionName
```

### Criterios de aceptación

- [ ] Versionado semántico configurado
- [ ] Versión visible en la app
- [ ] versionCode siempre incrementa

---

## Ejercicio 5: Analizar APK

### Instrucciones

Analiza el tamaño de tu APK y optimízalo.

### Pasos

1. Genera APK debug y release
2. Usa "Analyze APK" en Android Studio
3. Documenta:
   - Tamaño total
   - Tamaño de código (DEX)
   - Tamaño de recursos
   - Librerías más pesadas

4. Intenta reducir el tamaño:
   - Eliminar recursos no usados
   - Considerar splits por ABI

### Criterios de aceptación

- [ ] Análisis documentado
- [ ] Al menos una optimización aplicada
- [ ] Comparación antes/después

---

## Ejercicio 6: CI/CD básico

### Instrucciones

Configura GitHub Actions para compilar automáticamente.

### Requisitos

El workflow debe:
1. Ejecutarse en cada push a main
2. Compilar el proyecto
3. Ejecutar tests
4. Generar APK debug
5. Subir APK como artifact

### Archivo a crear

`.github/workflows/build.yml`

### Criterios de aceptación

- [ ] Workflow configurado
- [ ] Build pasa en GitHub Actions
- [ ] Tests se ejecutan
- [ ] APK disponible como artifact

---

## Ejercicio 7 (Bonus): Release automático

### Instrucciones

Configura release automático con tags.

### Requisitos

1. Al crear tag `v*`, el workflow debe:
   - Compilar release APK (firmado)
   - Crear GitHub Release
   - Adjuntar APK al release

2. Configurar secrets en GitHub:
   - KEYSTORE_BASE64
   - KEYSTORE_PASSWORD
   - KEY_ALIAS
   - KEY_PASSWORD

### Criterios de aceptación

- [ ] Secrets configurados en GitHub
- [ ] Al crear tag, se genera release
- [ ] APK firmado adjunto al release

---

## Proyecto final: Preparar app para distribución

### Instrucciones

Prepara una de tus apps del curso para distribución real.

### Checklist completo

**Configuración:**
- [ ] Keystore creado y respaldado
- [ ] Signing configurado
- [ ] ProGuard rules
- [ ] Versionado correcto

**Calidad:**
- [ ] Tests pasan
- [ ] No hay crashes conocidos
- [ ] Probado en dispositivo real

**Documentación:**
- [ ] README con instrucciones de build
- [ ] Changelog de la versión
- [ ] Capturas de pantalla

**Build:**
- [ ] APK release generado
- [ ] Tamaño optimizado
- [ ] mapping.txt guardado

---

## Entrega

1. Sube el proyecto a GitHub
2. Incluye:
   - APK release firmado (en Releases)
   - Workflow de CI funcionando
   - README con instrucciones
3. NO subas el keystore ni passwords
4. Crea PR con los cambios de configuración
