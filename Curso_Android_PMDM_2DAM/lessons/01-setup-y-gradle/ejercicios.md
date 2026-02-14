# Soluciones - Lección 01: Setup y Gradle

## Ejercicio 2: Modificar el Greeting

### Solución

```kotlin
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Column(modifier = modifier) {
        Text(text = "¡Hola, $name!")
        Text(text = "Asignatura: PMDM")
        Text(text = "Fecha: 01/02/2026")
    }
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyAppTheme {
        Greeting("Tu Nombre")
    }
}
```

**Imports necesarios:**
```kotlin
import androidx.compose.foundation.layout.Column
```

### Explicación

- `Column` es un layout que apila elementos verticalmente
- Cada `Text` es un composable que muestra texto
- El `modifier` se pasa al `Column` para que los modificadores externos funcionen

---

## Ejercicio 3: Añadir dependencia Coil

### Solución

**gradle/libs.versions.toml:**
```toml
[versions]
# ... otras versiones
coil = "2.5.0"

[libraries]
# ... otras librerías
coil-compose = { group = "io.coil-kt", name = "coil-compose", version.ref = "coil" }
```

**app/build.gradle.kts:**
```kotlin
dependencies {
    // ... otras dependencias
    implementation(libs.coil.compose)
}
```

### Explicación

El Version Catalog (`libs.versions.toml`) centraliza las versiones de dependencias. Esto:
- Evita duplicar versiones en múltiples archivos
- Facilita actualizar versiones
- Proporciona autocompletado en el IDE

---

## Ejercicio 4: Explorar estructura

### Respuestas

1. **¿Dónde se declara el nombre de la app?**
   - Archivo: `app/src/main/res/values/strings.xml`
   - Línea: `<string name="app_name">MiPrimerApp</string>`

2. **¿Qué archivo para cambiar el icono?**
   - Archivos: `app/src/main/res/mipmap-*/ic_launcher.png` y `ic_launcher_round.png`
   - También: `app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml` (adaptive icon)

3. **¿Cuál es el applicationId?**
   - Archivo: `app/build.gradle.kts`
   - Valor: `com.tuapellido.miprimerapp` (el que pusiste al crear)

4. **¿Qué versión de Kotlin?**
   - Archivo: `gradle/libs.versions.toml`
   - Busca: `kotlin = "X.X.X"` (normalmente 1.9.22 o similar)

5. **¿Qué compileSdk?**
   - Archivo: `app/build.gradle.kts`
   - Valor: `34` (o el que venga por defecto)

---

## Ejercicio 5: Comandos Gradle

### Respuestas

1. **`./gradlew tasks`**
   - Lista todas las tareas disponibles de Gradle
   - Útil para descubrir qué puedes hacer

2. **`./gradlew assembleDebug`**
   - Compila la versión debug de la app
   - Genera el APK

3. **`./gradlew test`**
   - Ejecuta los tests unitarios
   - Por defecto hay 0 tests (el proyecto nuevo no incluye ninguno real)

4. **`./gradlew lint`**
   - Analiza el código en busca de problemas
   - Genera un reporte HTML

5. **`./gradlew clean`**
   - Borra la carpeta `build/`
   - Útil cuando hay problemas de cache

### Ubicaciones

- **APK generado:** `app/build/outputs/apk/debug/app-debug.apk`
- **Reporte lint:** `app/build/reports/lint-results-debug.html`

---

## Ejercicio 6: Permiso de Internet

### Solución

**AndroidManifest.xml:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MiPrimerApp">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:label="@string/app_name"
            android:theme="@style/Theme.MiPrimerApp">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
```

### Explicación

El permiso `INTERNET` es necesario para cualquier comunicación de red. Debe estar:
- Dentro del tag `<manifest>`
- Fuera (antes) del tag `<application>`

Este es un permiso "normal" que se concede automáticamente al instalar. No requiere solicitud en tiempo de ejecución.

---

## Errores comunes

### Error: "Unresolved reference: Column"

**Causa:** Falta el import.

**Solución:** Añade `import androidx.compose.foundation.layout.Column`

### Error: Gradle sync failed después de añadir dependencia

**Posibles causas:**
1. Typo en el nombre de la dependencia
2. La versión no existe
3. Sin conexión a internet

**Solución:**
1. Revisa que el nombre coincide exactamente
2. Verifica la versión en Maven Central
3. Comprueba tu conexión

### Error: El APK no se encuentra

**Causa:** No has ejecutado `assembleDebug`.

**Solución:** Ejecuta `./gradlew assembleDebug` primero.

### Error: Lint falla con errores

**Causa:** Hay problemas de código que lint detecta.

**Solución:**
1. Abre el reporte HTML
2. Revisa los errores
3. Corrígelos o suprime si son falsos positivos
