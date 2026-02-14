# Solución de problemas

Guía de errores comunes y cómo resolverlos.

---

## Gradle Sync Failed

### Síntoma

Al abrir el proyecto, aparece un error rojo: "Gradle sync failed".

### Causas y soluciones

#### 1. Sin conexión a internet

Gradle necesita descargar dependencias la primera vez.

**Solución:** Conéctate a internet y haz **File → Sync Project with Gradle Files**.

#### 2. Proxy/firewall corporativo

El firewall bloquea las descargas de Maven.

**Solución:**
1. Configura el proxy en **File → Settings → Appearance & Behavior → System Settings → HTTP Proxy**
2. O usa una red sin restricciones

#### 3. Versión de Gradle incompatible

El proyecto usa una versión de Gradle que no tienes.

**Solución:**
1. Deja que Android Studio descargue la versión correcta (automático)
2. O manualmente: **File → Project Structure → Project → Gradle Version**

#### 4. JDK incorrecto

El proyecto necesita JDK 17 pero tienes otra versión.

**Solución:**
1. **File → Settings → Build → Gradle → Gradle JDK**
2. Selecciona **JDK 17** (Android Studio lo incluye)
3. Si no aparece, descárgalo: **Download JDK → Version 17**

#### 5. Cache corrupta

La cache de Gradle está corrupta.

**Solución:**
```bash
# Windows
rd /s /q %USERPROFILE%\.gradle\caches

# Mac/Linux  
rm -rf ~/.gradle/caches
```

Luego **File → Invalidate Caches → Invalidate and Restart**.

---

## SDK not found

### Síntoma

Error: "SDK location not found" o "Failed to find target".

### Solución

1. **File → Project Structure → SDK Location**
2. Verifica que **Android SDK location** apunta a tu SDK:
   - Windows: `C:\Users\TU_USUARIO\AppData\Local\Android\Sdk`
   - Mac: `~/Library/Android/sdk`
   - Linux: `~/Android/Sdk`
3. Si no existe, abre **SDK Manager** e instala el SDK

### Si instalaste en ubicación no estándar

Crea un archivo `local.properties` en la raíz del proyecto:

```properties
sdk.dir=C:\\ruta\\a\\tu\\Android\\Sdk
```

(En Windows usa `\\` o `/`, no `\` solo)

---

## Kotlin version mismatch

### Síntoma

Error: "Module was compiled with an incompatible version of Kotlin".

### Solución

1. Abre `build.gradle.kts` (proyecto, no módulo)
2. Busca la versión de Kotlin:
   ```kotlin
   plugins {
       kotlin("android") version "1.9.22"
   }
   ```
3. Asegúrate de que tu Android Studio tiene el plugin de Kotlin actualizado:
   - **File → Settings → Plugins → Kotlin**
   - Actualiza si hay nueva versión
4. **File → Sync Project with Gradle Files**

---

## Emulador lento

### Síntoma

El emulador tarda mucho en arrancar o la app va muy lenta.

### Soluciones

#### 1. Habilitar aceleración de hardware

**Windows:**
1. Verifica que tienes Intel HAXM o Windows Hypervisor Platform
2. **SDK Manager → SDK Tools → Intel x86 Emulator Accelerator (HAXM)**
3. Instálalo y reinicia

**BIOS:**
1. Entra en BIOS (F2, F12, Del al arrancar)
2. Busca "Intel VT-x" o "AMD-V" o "Virtualization"
3. Habilítalo
4. Guarda y reinicia

**Linux:**
```bash
sudo apt install qemu-kvm
sudo adduser $USER kvm
# Reinicia sesión
```

#### 2. Usar imagen x86_64

1. **AVD Manager → Create Device**
2. Al elegir System Image, selecciona **x86_64**, no ARM
3. Las imágenes ARM son mucho más lentas

#### 3. Asignar más RAM al emulador

1. **AVD Manager → Edit (lápiz) junto a tu dispositivo**
2. **Show Advanced Settings**
3. **RAM:** 2048 MB o más
4. **VM heap:** 512 MB

#### 4. Usar Cold Boot

Si el emulador se queda colgado:
1. **AVD Manager → menú ▼ junto al dispositivo → Cold Boot Now**

#### 5. Alternativa: dispositivo físico

Conecta tu móvil Android por USB:
1. Habilita **Opciones de desarrollador** (toca 7 veces en Número de compilación)
2. Activa **Depuración USB**
3. Conecta el cable y acepta la autorización
4. Aparecerá en el desplegable de dispositivos

---

## "R" class not found / Unresolved reference R

### Síntoma

Android Studio marca en rojo `R.layout`, `R.string`, etc.

### Solución

1. **Build → Clean Project**
2. **Build → Rebuild Project**
3. Si persiste: **File → Invalidate Caches → Invalidate and Restart**

### Si sigue fallando

Revisa que no haya errores en los archivos XML de recursos:
- `res/layout/*.xml`
- `res/values/*.xml`

Un solo error XML impide generar la clase R.

---

## Cannot resolve symbol 'XXX'

### Síntoma

Imports marcados en rojo, clases no encontradas.

### Solución por tipo

#### Dependencia no añadida

Si es una librería externa (Retrofit, Room, etc.):

1. Verifica que está en `build.gradle.kts` (módulo app):
   ```kotlin
   dependencies {
       implementation("com.squareup.retrofit2:retrofit:2.9.0")
   }
   ```
2. **Sync Project with Gradle Files**

#### Clase del proyecto

Si es una clase tuya:

1. Verifica que el archivo existe
2. Verifica que el package es correcto
3. **Build → Rebuild Project**

#### Clase de Android

1. Verifica que tienes el SDK correcto instalado
2. **File → Sync Project with Gradle Files**

---

## App crashes on launch

### Síntoma

La app se instala pero se cierra inmediatamente.

### Diagnóstico

1. Abre **Logcat** (pestaña abajo en Android Studio)
2. Filtra por nivel **Error**
3. Busca el mensaje "FATAL EXCEPTION"
4. Lee el stack trace

### Causas comunes

#### NullPointerException

Algo es `null` cuando no debería. Lee el stack trace para ver qué línea.

#### ActivityNotFoundException

Falta declarar una Activity en `AndroidManifest.xml`:

```xml
<activity android:name=".DetailActivity" />
```

#### NetworkOnMainThreadException

Estás haciendo llamadas de red en el hilo principal.

**Solución:** Usa coroutines con `Dispatchers.IO`:

```kotlin
viewModelScope.launch(Dispatchers.IO) {
    val data = api.getData()
}
```

#### Missing permission

Falta un permiso en el manifest:

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

---

## Tests fallan en CI pero pasan en local

### Causas comunes

#### 1. Dependencia de hora/fecha

Los tests dependen de la hora actual.

**Solución:** Inyecta un `Clock` mockeado en tests.

#### 2. Dependencia de orden

Los tests dependen del orden de ejecución.

**Solución:** Cada test debe ser independiente. Usa `@Before` para setup.

#### 3. Paths absolutos

El código usa paths que solo existen en tu máquina.

**Solución:** Usa paths relativos o recursos del classpath.

#### 4. Locale diferente

El CI usa locale inglés, tu máquina español.

**Solución:** No dependas del locale para formatear/parsear.

---

## Lint errors

### Síntoma

CI falla con errores de lint.

### Ver errores

```bash
./gradlew lint
```

El reporte se genera en: `app/build/reports/lint-results.html`

### Errores comunes

#### HardcodedText

Texto directamente en el código en lugar de `strings.xml`.

```kotlin
// Mal
Text("Hola mundo")

// Bien
Text(stringResource(R.string.hello_world))
```

#### UnusedResources

Recursos en `res/` que no se usan. Elimínalos o añade:

```kotlin
@Suppress("UnusedResources")
```

#### Obsolete API

Usas APIs deprecadas.

**Solución:** Actualiza al API nuevo que sugiere lint.

### Suprimir lint (solo si es necesario)

```kotlin
@SuppressLint("HardcodedText")
fun myFunction() { ... }
```

En `build.gradle.kts`:
```kotlin
android {
    lint {
        disable += "HardcodedText"
    }
}
```

---

## Compose Preview no funciona

### Síntoma

Los previews de Compose no se renderizan.

### Solución

1. Verifica que la función tiene `@Preview`:
   ```kotlin
   @Preview(showBackground = true)
   @Composable
   fun MyPreview() {
       MyComponent()
   }
   ```

2. **Build → Make Project** (Ctrl+F9)

3. La función de preview NO debe tener parámetros:
   ```kotlin
   // Mal - tiene parámetro
   @Preview
   @Composable
   fun MyPreview(name: String) { }
   
   // Bien - sin parámetros
   @Preview
   @Composable
   fun MyPreview() {
       MyComponent(name = "Test")
   }
   ```

4. Reinicia Android Studio si nada funciona

---

## Room: Schema export error

### Síntoma

Error: "Schema export directory is not provided".

### Solución

En `build.gradle.kts` (módulo app):

```kotlin
android {
    defaultConfig {
        ksp {
            arg("room.schemaLocation", "$projectDir/schemas")
        }
    }
}
```

O si no necesitas exportar schemas (desarrollo):

```kotlin
@Database(
    entities = [...],
    version = 1,
    exportSchema = false  // Añade esto
)
```

---

## Retrofit: Network error

### Síntoma

Las llamadas a la API fallan con "UnknownHostException" o "SocketTimeoutException".

### Soluciones

#### 1. Falta permiso de internet

```xml
<!-- AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
```

#### 2. HTTP en lugar de HTTPS

Android bloquea HTTP por defecto.

**Solución A:** Usa HTTPS.

**Solución B:** Permite cleartext (solo desarrollo):

```xml
<!-- AndroidManifest.xml -->
<application
    android:usesCleartextTraffic="true"
    ... >
```

#### 3. Emulador sin internet

1. Verifica tu conexión real
2. Reinicia el emulador
3. O: **AVD Manager → Wipe Data** y reinicia

---

## "Could not determine the dependencies of task ':app:compileDebugKotlin'"

### Síntoma

Error críptico de Gradle sobre dependencias.

### Solución

1. **File → Invalidate Caches → Invalidate and Restart**
2. Borra `.gradle` del proyecto:
   ```bash
   rm -rf .gradle/
   ```
3. **File → Sync Project with Gradle Files**

---

## Contacto

Si tu problema no está aquí:

1. Busca el mensaje exacto del error en Google
2. Revisa Stack Overflow
3. Abre un Issue en el repositorio con:
   - Mensaje de error completo
   - Pasos para reproducir
   - Versión de Android Studio
   - Sistema operativo
