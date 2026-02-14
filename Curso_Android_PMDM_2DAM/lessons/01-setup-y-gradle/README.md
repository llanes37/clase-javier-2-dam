# Lección 01: Setup y Gradle

## Objetivos

- Verificar que Android Studio está correctamente instalado
- Entender la estructura de un proyecto Android
- Conocer el sistema de build Gradle
- Añadir dependencias al proyecto
- Ejecutar una app en el emulador

---

## 1. Verificación del entorno

Antes de continuar, asegúrate de tener:

- [ ] Android Studio instalado (ver [docs/01-instalacion-android-studio.md](../../docs/01-instalacion-android-studio.md))
- [ ] SDK 34 instalado
- [ ] Emulador configurado (Pixel 7, API 34)
- [ ] Git instalado y configurado

### Test rápido

1. Abre Android Studio
2. **File → New → New Project**
3. Selecciona **Empty Activity** (Compose)
4. Nombre: `TestSetup`
5. Package: `com.example.testsetup`
6. **Finish** y espera al Gradle Sync
7. Run → Run 'app'

Si ves "Hello Android!" en el emulador, ¡todo funciona!

---

## 2. Estructura de un proyecto Android

Cuando abres un proyecto, verás esta estructura:

```
MyApp/
├── app/                          # Módulo principal de la app
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/             # Código Kotlin (sí, carpeta "java")
│   │   │   │   └── com/example/myapp/
│   │   │   │       └── MainActivity.kt
│   │   │   ├── res/              # Recursos (layouts, strings, etc.)
│   │   │   │   ├── drawable/
│   │   │   │   ├── mipmap/       # Iconos de la app
│   │   │   │   └── values/
│   │   │   │       ├── strings.xml
│   │   │   │       ├── colors.xml
│   │   │   │       └── themes.xml
│   │   │   └── AndroidManifest.xml
│   │   ├── test/                 # Tests unitarios
│   │   └── androidTest/          # Tests de instrumentación
│   └── build.gradle.kts          # Config del módulo app
├── gradle/
│   └── wrapper/
│       └── gradle-wrapper.properties
├── build.gradle.kts              # Config del proyecto
├── settings.gradle.kts           # Módulos incluidos
└── local.properties              # Rutas locales (SDK)
```

### Archivos clave

| Archivo | Propósito |
|---------|-----------|
| `AndroidManifest.xml` | Declara activities, permisos, metadatos |
| `build.gradle.kts` (app) | Dependencias, SDK versions, plugins |
| `build.gradle.kts` (raíz) | Config global, versiones de plugins |
| `settings.gradle.kts` | Define qué módulos incluir |
| `MainActivity.kt` | Punto de entrada de la app |

---

## 3. AndroidManifest.xml

El manifest declara los componentes de tu app:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Permisos que necesita la app -->
    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.MyApp">

        <!-- Activity principal -->
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>
</manifest>
```

**Puntos importantes:**
- `android:exported="true"` es obligatorio para la activity lanzadora
- El `intent-filter` con MAIN + LAUNCHER hace que aparezca en el menú
- Los permisos se declaran fuera del tag `<application>`

---

## 4. Sistema de build Gradle

Gradle es el sistema que compila tu proyecto, gestiona dependencias y genera el APK.

### build.gradle.kts (módulo app)

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
}

android {
    namespace = "com.example.myapp"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    // Core Android
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)

    // Compose
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)

    // Testing
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
}
```

### Conceptos clave

| Concepto | Descripción |
|----------|-------------|
| `compileSdk` | SDK usado para compilar (usa el más reciente) |
| `minSdk` | Mínimo Android soportado (API 26 = Android 8.0) |
| `targetSdk` | SDK objetivo (comportamientos nuevos) |
| `implementation` | Dependencia incluida en el APK |
| `testImplementation` | Solo para tests |
| `BOM` (Bill of Materials) | Gestiona versiones compatibles de Compose |

---

## 5. Añadir dependencias

### Paso 1: Buscar la dependencia

Ve a [Maven Central](https://search.maven.org/) o [Google Maven](https://maven.google.com/web/index.html).

### Paso 2: Añadir al version catalog

En `gradle/libs.versions.toml`:

```toml
[versions]
retrofit = "2.9.0"

[libraries]
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
```

### Paso 3: Usar en build.gradle.kts

```kotlin
dependencies {
    implementation(libs.retrofit)
}
```

### Paso 4: Sync

Clic en **Sync Now** o **File → Sync Project with Gradle Files**.

---

## 6. Tareas Gradle comunes

Desde terminal o desde la pestaña Gradle de Android Studio:

```bash
# Compilar debug
./gradlew assembleDebug

# Ejecutar tests
./gradlew test

# Lint (análisis estático)
./gradlew lint

# Limpiar build
./gradlew clean

# Ver dependencias
./gradlew app:dependencies
```

---

## 7. MainActivity con Compose

Un proyecto Compose nuevo tiene esta estructura:

```kotlin
package com.example.myapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.myapp.ui.theme.MyAppTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyAppTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    Greeting("Android")
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MyAppTheme {
        Greeting("Android")
    }
}
```

**Puntos clave:**
- `setContent { }` reemplaza a `setContentView()` de XML
- `@Composable` marca funciones que definen UI
- `@Preview` permite ver la UI sin ejecutar la app

---

## 8. Ejecución y depuración

### Ejecutar en emulador

1. Selecciona el emulador en el desplegable
2. Clic en ▶️ **Run 'app'** (o Shift+F10)
3. Espera a que compile e instale

### Ejecutar en dispositivo físico

1. Habilita **Opciones de desarrollador** en tu móvil
2. Activa **Depuración USB**
3. Conecta por USB
4. Acepta la autorización en el móvil
5. Selecciona el dispositivo y ejecuta

### Depuración

1. Pon un breakpoint (clic en el margen izquierdo)
2. Clic en 🐛 **Debug 'app'** (o Shift+F9)
3. Usa Step Over (F8), Step Into (F7), Resume (F9)

---

## Resumen

| Concepto | Qué es |
|----------|--------|
| Gradle | Sistema de build que compila y gestiona dependencias |
| Manifest | Declara componentes, permisos y metadatos de la app |
| build.gradle.kts | Configura SDK, dependencias y opciones de compilación |
| compileSdk vs targetSdk | compileSdk = para compilar, targetSdk = comportamiento |
| setContent | Punto de entrada de Compose en una Activity |

---

## Siguiente paso

→ [ejercicios.md](ejercicios.md)
