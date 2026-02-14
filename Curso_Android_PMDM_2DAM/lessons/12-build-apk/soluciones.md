# Soluciones - Lección 12: Generar APK y distribución

## Ejercicio 1: Configurar build types

```kotlin
// build.gradle.kts (app)
android {
    namespace = "com.example.miapp"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.miapp"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        debug {
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            isDebuggable = true
        }
        
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            isDebuggable = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

---

## Ejercicio 2: Crear y configurar keystore

### Crear keystore

```bash
keytool -genkey -v \
  -keystore release-keystore.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias release
```

### local.properties

```properties
# NO subir a Git
KEYSTORE_FILE=../keystore/release-keystore.jks
KEYSTORE_PASSWORD=tu_password_seguro
KEY_ALIAS=release
KEY_PASSWORD=tu_key_password
```

### .gitignore

```gitignore
# Keystore
*.jks
*.keystore
local.properties
```

### build.gradle.kts

```kotlin
import java.util.Properties

val localProperties = Properties().apply {
    val file = rootProject.file("local.properties")
    if (file.exists()) load(file.inputStream())
}

android {
    signingConfigs {
        create("release") {
            val keystoreFile = localProperties.getProperty("KEYSTORE_FILE", "")
            if (keystoreFile.isNotEmpty()) {
                storeFile = file(keystoreFile)
                storePassword = localProperties.getProperty("KEYSTORE_PASSWORD", "")
                keyAlias = localProperties.getProperty("KEY_ALIAS", "")
                keyPassword = localProperties.getProperty("KEY_PASSWORD", "")
            }
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

---

## Ejercicio 3: ProGuard rules

```proguard
# proguard-rules.pro

# ========== GENERAL ==========

# Mantener atributos importantes
-keepattributes Signature
-keepattributes *Annotation*
-keepattributes SourceFile,LineNumberTable
-keepattributes InnerClasses,EnclosingMethod

# ========== MODELOS ==========

# Mantener todas las data classes del paquete model
-keep class com.example.miapp.data.model.** { *; }
-keep class com.example.miapp.domain.model.** { *; }

# ========== RETROFIT ==========

-dontwarn retrofit2.**
-keep class retrofit2.** { *; }
-keepclasseswithmembers class * {
    @retrofit2.http.* <methods>;
}

# ========== MOSHI ==========

-keep class com.squareup.moshi.** { *; }
-keep @com.squareup.moshi.JsonClass class * { *; }
-keepclassmembers class * {
    @com.squareup.moshi.FromJson <methods>;
    @com.squareup.moshi.ToJson <methods>;
}

# ========== ROOM ==========

-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *
-dontwarn androidx.room.paging.**

# ========== COROUTINES ==========

-keepnames class kotlinx.coroutines.internal.MainDispatcherFactory {}
-keepnames class kotlinx.coroutines.CoroutineExceptionHandler {}

# ========== COMPOSE ==========

# Compose generalmente no necesita reglas especiales
# pero por si acaso:
-keep class androidx.compose.** { *; }

# ========== OKHTTP ==========

-dontwarn okhttp3.**
-dontwarn okio.**
-keep class okhttp3.** { *; }
-keep interface okhttp3.** { *; }

# ========== DEBUG ==========

# Para facilitar debugging de crashes
-renamesourcefileattribute SourceFile
```

---

## Ejercicio 4: Versionado

```kotlin
// build.gradle.kts (app)
android {
    defaultConfig {
        versionCode = 3          // Incrementar en cada release
        versionName = "1.1.0"    // Semantic versioning
    }
}

// AppVersion.kt - para acceder desde código
object AppVersion {
    fun getVersionName(context: Context): String {
        return try {
            context.packageManager
                .getPackageInfo(context.packageName, 0)
                .versionName ?: "Unknown"
        } catch (e: Exception) {
            "Unknown"
        }
    }
    
    fun getVersionCode(context: Context): Long {
        return try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                context.packageManager
                    .getPackageInfo(context.packageName, 0)
                    .longVersionCode
            } else {
                @Suppress("DEPRECATION")
                context.packageManager
                    .getPackageInfo(context.packageName, 0)
                    .versionCode.toLong()
            }
        } catch (e: Exception) {
            0
        }
    }
}

// AboutScreen.kt
@Composable
fun AboutScreen() {
    val context = LocalContext.current
    val versionName = remember { AppVersion.getVersionName(context) }
    
    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            "Mi App",
            style = MaterialTheme.typography.headlineLarge
        )
        
        Spacer(Modifier.height(16.dp))
        
        Text(
            "Versión $versionName",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
```

---

## Ejercicio 5: Analizar APK

### Script de análisis

```bash
#!/bin/bash
# analyze-apk.sh

echo "=== Generando APKs ==="
./gradlew assembleDebug assembleRelease

DEBUG_APK="app/build/outputs/apk/debug/app-debug.apk"
RELEASE_APK="app/build/outputs/apk/release/app-release.apk"

echo ""
echo "=== Tamaños ==="
echo "Debug APK: $(du -h $DEBUG_APK | cut -f1)"
echo "Release APK: $(du -h $RELEASE_APK | cut -f1)"

echo ""
echo "=== Para análisis detallado ==="
echo "Abre Android Studio -> Build -> Analyze APK"
echo "Selecciona: $RELEASE_APK"
```

### Documentación de análisis

```markdown
# Análisis de APK - Mi App

## Tamaños
- Debug APK: 8.5 MB
- Release APK: 3.2 MB
- Reducción: 62%

## Desglose Release APK
- DEX (código): 1.8 MB
- Resources: 0.9 MB
- Native libs: 0.3 MB
- Otros: 0.2 MB

## Librerías más pesadas
1. Compose UI: ~800 KB
2. Material 3: ~400 KB
3. Retrofit + OkHttp: ~300 KB

## Optimizaciones aplicadas
1. ✅ Minify enabled
2. ✅ Shrink resources
3. ✅ ProGuard optimizations
4. ⏳ Considerar splits por ABI (no implementado)
```

---

## Ejercicio 6: CI/CD básico

```yaml
# .github/workflows/build.yml
name: Android Build

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: 'gradle'
      
      - name: Grant execute permission for gradlew
        run: chmod +x gradlew
      
      - name: Run unit tests
        run: ./gradlew test
      
      - name: Build debug APK
        run: ./gradlew assembleDebug
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: app/build/reports/tests/
      
      - name: Upload debug APK
        uses: actions/upload-artifact@v3
        with:
          name: app-debug
          path: app/build/outputs/apk/debug/app-debug.apk
```

---

## Ejercicio 7: Release automático

```yaml
# .github/workflows/release.yml
name: Release Build

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
          cache: 'gradle'
      
      - name: Grant execute permission
        run: chmod +x gradlew
      
      - name: Decode Keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > keystore.jks
      
      - name: Run tests
        run: ./gradlew test
      
      - name: Build Release APK
        env:
          KEYSTORE_FILE: ${{ github.workspace }}/keystore.jks
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: ./gradlew assembleRelease
      
      - name: Get version from tag
        id: get_version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          name: Release ${{ steps.get_version.outputs.VERSION }}
          files: |
            app/build/outputs/apk/release/app-release.apk
          body: |
            ## What's New
            - Release version ${{ steps.get_version.outputs.VERSION }}
            
            ## Installation
            Download the APK and install on your Android device.
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Upload mapping file
        uses: actions/upload-artifact@v3
        with:
          name: mapping-${{ steps.get_version.outputs.VERSION }}
          path: app/build/outputs/mapping/release/mapping.txt
```

### Configurar secrets

```bash
# Codificar keystore en base64
base64 -i keystore.jks -o keystore_base64.txt

# En GitHub: Settings -> Secrets and variables -> Actions
# Añadir:
# - KEYSTORE_BASE64: contenido de keystore_base64.txt
# - KEYSTORE_PASSWORD: tu password
# - KEY_ALIAS: release
# - KEY_PASSWORD: tu key password
```

### Crear release

```bash
# Crear y subir tag
git tag v1.0.0
git push origin v1.0.0

# El workflow se ejecutará automáticamente
# y creará el release con el APK
```
