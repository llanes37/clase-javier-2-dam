# Lección 12: Generar APK y distribución

## Objetivos

- Entender tipos de build (debug/release)
- Configurar signing para release
- Generar APK y AAB
- Optimizar tamaño de la app
- Preparar para distribución

---

## 1. Debug vs Release

| Aspecto | Debug | Release |
|---------|-------|---------|
| Firma | Automática (debug key) | Requiere keystore propio |
| Optimización | No | ProGuard/R8 |
| Debuggable | Sí | No |
| Uso | Desarrollo | Producción |

---

## 2. Configurar build types

```kotlin
// build.gradle.kts (app)
android {
    buildTypes {
        debug {
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            isDebuggable = true
        }
        
        release {
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

## 3. Crear Keystore

### Desde Android Studio

1. Build → Generate Signed Bundle/APK
2. Create new... (si no tienes keystore)
3. Rellenar:
   - Key store path: `/ruta/mi-keystore.jks`
   - Password: (contraseña segura)
   - Alias: `mi-alias`
   - Key password: (contraseña segura)
   - Validity: 25 años mínimo

### Desde terminal

```bash
keytool -genkey -v -keystore mi-keystore.jks -keyalg RSA -keysize 2048 -validity 9125 -alias mi-alias
```

### ⚠️ IMPORTANTE

- **Guarda el keystore en lugar seguro**
- **Nunca pierdas el keystore** (no podrás actualizar la app)
- **No subas el keystore a Git**

---

## 4. Configurar signing

### Opción A: En build.gradle (NO recomendado para producción)

```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("../keystore/mi-keystore.jks")
            storePassword = "password"
            keyAlias = "mi-alias"
            keyPassword = "password"
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            // ...
        }
    }
}
```

### Opción B: Con variables de entorno (recomendado)

```kotlin
// build.gradle.kts (app)
android {
    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("KEYSTORE_FILE") ?: "../keystore/release.jks")
            storePassword = System.getenv("KEYSTORE_PASSWORD") ?: ""
            keyAlias = System.getenv("KEY_ALIAS") ?: ""
            keyPassword = System.getenv("KEY_PASSWORD") ?: ""
        }
    }
}
```

### Opción C: Con local.properties (para desarrollo local)

```properties
# local.properties (NO subir a Git)
KEYSTORE_FILE=../keystore/mi-keystore.jks
KEYSTORE_PASSWORD=mi_password
KEY_ALIAS=mi-alias
KEY_PASSWORD=mi_password
```

```kotlin
// build.gradle.kts (app)
import java.util.Properties

val localProperties = Properties().apply {
    val file = rootProject.file("local.properties")
    if (file.exists()) load(file.inputStream())
}

android {
    signingConfigs {
        create("release") {
            storeFile = file(localProperties.getProperty("KEYSTORE_FILE", ""))
            storePassword = localProperties.getProperty("KEYSTORE_PASSWORD", "")
            keyAlias = localProperties.getProperty("KEY_ALIAS", "")
            keyPassword = localProperties.getProperty("KEY_PASSWORD", "")
        }
    }
}
```

---

## 5. Generar APK

### Desde Android Studio

1. Build → Build Bundle(s) / APK(s) → Build APK(s)
2. O: Build → Generate Signed Bundle/APK → APK

### Desde terminal

```bash
# Debug APK
./gradlew assembleDebug

# Release APK
./gradlew assembleRelease

# Ubicación del APK
# app/build/outputs/apk/release/app-release.apk
```

---

## 6. Generar AAB (Android App Bundle)

Recomendado para Google Play Store:

### Desde Android Studio

1. Build → Generate Signed Bundle/APK → Android App Bundle

### Desde terminal

```bash
./gradlew bundleRelease

# Ubicación
# app/build/outputs/bundle/release/app-release.aab
```

### Ventajas del AAB

- Google Play optimiza para cada dispositivo
- Menor tamaño de descarga
- Requerido para nuevas apps en Play Store

---

## 7. ProGuard/R8

### Reglas básicas

```proguard
# proguard-rules.pro

# Mantener clases de modelo (para serialización)
-keep class com.example.app.data.model.** { *; }

# Mantener anotaciones
-keepattributes *Annotation*

# Retrofit
-keepattributes Signature
-keepattributes Exceptions
-keep class retrofit2.** { *; }
-keepclasseswithmembers class * {
    @retrofit2.http.* <methods>;
}

# Moshi
-keep class com.squareup.moshi.** { *; }
-keepclassmembers class * {
    @com.squareup.moshi.* <methods>;
}

# Room
-keep class * extends androidx.room.RoomDatabase
-keep @androidx.room.Entity class *

# Compose (generalmente no necesita reglas extra)
```

### Verificar que funciona

```bash
# Generar mapping file
./gradlew assembleRelease

# El archivo mapping.txt está en:
# app/build/outputs/mapping/release/mapping.txt
# Guárdalo para poder desofuscar stack traces
```

---

## 8. Optimizar tamaño

### Habilitar shrinking

```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true      // Eliminar código no usado
            isShrinkResources = true    // Eliminar recursos no usados
        }
    }
}
```

### Splits por ABI (opcional)

```kotlin
android {
    splits {
        abi {
            isEnable = true
            reset()
            include("armeabi-v7a", "arm64-v8a", "x86", "x86_64")
            isUniversalApk = false
        }
    }
}
```

### Analizar APK

En Android Studio: Build → Analyze APK

---

## 9. Versionado

```kotlin
// build.gradle.kts (app)
android {
    defaultConfig {
        versionCode = 1          // Incrementar en cada release
        versionName = "1.0.0"    // Visible para usuarios
    }
}
```

### Convención de versiones

```
versionName: MAJOR.MINOR.PATCH
- MAJOR: Cambios incompatibles
- MINOR: Nueva funcionalidad compatible
- PATCH: Bug fixes

versionCode: Siempre incrementar (1, 2, 3...)
```

---

## 10. GitHub Actions para build

```yaml
# .github/workflows/release.yml
name: Build Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Decode Keystore
        run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > keystore.jks
      
      - name: Build Release APK
        env:
          KEYSTORE_FILE: keystore.jks
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: ./gradlew assembleRelease
      
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: app-release
          path: app/build/outputs/apk/release/app-release.apk
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: app/build/outputs/apk/release/app-release.apk
```

### Configurar secrets en GitHub

1. Repository → Settings → Secrets
2. Añadir:
   - `KEYSTORE_BASE64`: `base64 keystore.jks`
   - `KEYSTORE_PASSWORD`
   - `KEY_ALIAS`
   - `KEY_PASSWORD`

---

## 11. Distribución

### Google Play Store

1. Crear cuenta de desarrollador (25$ una vez)
2. Crear app en Play Console
3. Subir AAB
4. Rellenar información de la app
5. Enviar a revisión

### Firebase App Distribution

Para testing interno:

```yaml
- name: Upload to Firebase
  uses: wzieba/Firebase-Distribution-Github-Action@v1
  with:
    appId: ${{ secrets.FIREBASE_APP_ID }}
    serviceCredentialsFileContent: ${{ secrets.FIREBASE_SERVICE_ACCOUNT }}
    groups: testers
    file: app/build/outputs/apk/release/app-release.apk
```

### Distribución directa

- Compartir APK por email/drive
- Requiere "Permitir fuentes desconocidas" en el dispositivo

---

## Resumen: Pasos para release

1. **Crear keystore** (solo una vez)
2. **Configurar signing** en build.gradle
3. **Actualizar versionCode y versionName**
4. **Generar APK/AAB firmado**
5. **Probar en dispositivo real**
6. **Distribuir**

### Checklist pre-release

- [ ] versionCode incrementado
- [ ] versionName actualizado
- [ ] Tests pasan
- [ ] ProGuard configurado
- [ ] APK probado en dispositivo
- [ ] Keystore respaldado
- [ ] Mapping file guardado

---

## Siguiente paso

¡Felicidades! Has completado el curso. Ahora puedes:

1. Completar el proyecto final
2. Publicar tu app
3. Seguir aprendiendo: Hilt, Compose avanzado, Kotlin Multiplatform
