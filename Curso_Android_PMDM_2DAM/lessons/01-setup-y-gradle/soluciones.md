# Ejercicios - Lección 01: Setup y Gradle

## Ejercicio 1: Crear proyecto desde cero

### Instrucciones

1. Crea un nuevo proyecto en Android Studio:
   - Template: **Empty Activity** (Compose)
   - Nombre: `MiPrimerApp`
   - Package: `com.tuapellido.miprimerapp`
   - minSdk: 26
   - Build config language: Kotlin DSL

2. Espera a que termine el Gradle Sync

3. Ejecuta la app en el emulador

### Criterios de aceptación

- [ ] El proyecto compila sin errores
- [ ] La app se ejecuta en el emulador
- [ ] Se muestra "Hello Android!" en pantalla

---

## Ejercicio 2: Modificar el Greeting

### Instrucciones

1. Abre `MainActivity.kt`
2. Modifica la función `Greeting` para que muestre:
   - Tu nombre
   - El nombre de la asignatura
   - La fecha actual

3. La UI debe mostrar algo como:
   ```
   ¡Hola, [Tu Nombre]!
   Asignatura: PMDM
   Fecha: 01/02/2026
   ```

### Pistas

- Usa `Column` para apilar textos verticalmente:
  ```kotlin
  Column {
      Text("Línea 1")
      Text("Línea 2")
  }
  ```

- Necesitarás importar:
  ```kotlin
  import androidx.compose.foundation.layout.Column
  ```

### Criterios de aceptación

- [ ] Se muestran 3 líneas de texto
- [ ] La información es correcta
- [ ] La Preview también funciona

---

## Ejercicio 3: Añadir una dependencia

### Instrucciones

1. Añade la dependencia de **Coil** (librería para cargar imágenes) al proyecto

2. En `gradle/libs.versions.toml`, añade:
   ```toml
   [versions]
   coil = "2.5.0"

   [libraries]
   coil-compose = { group = "io.coil-kt", name = "coil-compose", version.ref = "coil" }
   ```

3. En `app/build.gradle.kts`, añade:
   ```kotlin
   dependencies {
       implementation(libs.coil.compose)
       // ... resto de dependencias
   }
   ```

4. Haz Sync

5. Verifica que compila ejecutando:
   ```bash
   ./gradlew assembleDebug
   ```

### Criterios de aceptación

- [ ] Gradle Sync completa sin errores
- [ ] El proyecto compila
- [ ] Puedes ver `coil-compose` en las dependencias externas

---

## Ejercicio 4: Explorar estructura del proyecto

### Instrucciones

Responde a estas preguntas explorando tu proyecto:

1. ¿Dónde se declara el nombre de la app que aparece en el launcher?

2. ¿Qué archivo tendrías que modificar para cambiar el icono de la app?

3. ¿Cuál es el `applicationId` de tu app?

4. ¿Qué versión de Kotlin usa el proyecto?

5. ¿Qué `compileSdk` tiene configurado?

### Formato de respuesta

Crea un archivo `respuestas-ejercicio4.md` en la raíz del proyecto con tus respuestas.

### Criterios de aceptación

- [ ] Las 5 respuestas son correctas
- [ ] Incluyes la ruta del archivo donde encontraste cada respuesta

---

## Ejercicio 5: Comandos Gradle

### Instrucciones

Ejecuta los siguientes comandos desde la terminal (en la raíz del proyecto) y anota qué hace cada uno:

1. `./gradlew tasks`
2. `./gradlew assembleDebug`
3. `./gradlew test`
4. `./gradlew lint`
5. `./gradlew clean`

### Preguntas

1. ¿Dónde se genera el APK después de `assembleDebug`?
2. ¿Qué tipo de archivo genera `lint` y dónde está?
3. ¿Cuántos tests pasan con `test`?

### Criterios de aceptación

- [ ] Has ejecutado los 5 comandos
- [ ] Sabes dónde encontrar el APK generado
- [ ] Sabes dónde encontrar el reporte de lint

---

## Ejercicio 6 (Bonus): Añadir permiso de Internet

### Instrucciones

1. Añade el permiso de Internet al `AndroidManifest.xml`

2. Verifica que el permiso está correctamente añadido:
   - El permiso debe estar FUERA del tag `<application>`
   - Debe estar DENTRO del tag `<manifest>`

### Pista

```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### Criterios de aceptación

- [ ] El manifest es XML válido
- [ ] El permiso está en la ubicación correcta
- [ ] El proyecto sigue compilando

---

## Entrega

Para entregar estos ejercicios:

1. Crea una rama: `git checkout -b ejercicios/leccion-01-tu-nombre`
2. Haz commits de tus cambios
3. Push y abre un PR

Los ejercicios se evalúan como parte de la participación (30% de la nota final).
