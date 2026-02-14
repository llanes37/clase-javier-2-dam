# Instalación de Android Studio

## Requisitos del sistema

### Mínimos

| Sistema | RAM | Disco | Resolución |
|---------|-----|-------|------------|
| Windows 10/11 (64-bit) | 8 GB | 15 GB | 1280x800 |
| macOS 10.14+ | 8 GB | 15 GB | 1280x800 |
| Linux (64-bit) | 8 GB | 15 GB | 1280x800 |

### Recomendados

- 16 GB RAM
- SSD con 30 GB libres
- Procesador con soporte de virtualización (Intel VT-x / AMD-V)

---

## Paso 1: Descargar Android Studio

1. Ve a [developer.android.com/studio](https://developer.android.com/studio)
2. Descarga la versión estable (no Canary ni Beta)
3. Tamaño aproximado: 1 GB

---

## Paso 2: Instalar Android Studio

### Windows

1. Ejecuta el `.exe` descargado
2. Acepta el UAC si aparece
3. **Componentes a instalar:**
   - ✅ Android Studio
   - ✅ Android Virtual Device
4. Ruta de instalación: deja la por defecto o usa una sin espacios
5. Haz clic en Install y espera

### macOS

1. Abre el `.dmg` descargado
2. Arrastra Android Studio a Applications
3. Abre Android Studio desde Applications
4. Si aparece aviso de seguridad: Preferencias del Sistema → Seguridad → Abrir igualmente

### Linux

```bash
# Extrae el archivo
tar -xzf android-studio-*.tar.gz

# Mueve a /opt
sudo mv android-studio /opt/

# Ejecuta el instalador
/opt/android-studio/bin/studio.sh
```

---

## Paso 3: Configuración inicial (Setup Wizard)

Al abrir Android Studio por primera vez:

### 3.1 Import Settings

- Selecciona **Do not import settings** (instalación limpia)

### 3.2 Install Type

- Selecciona **Standard** (instala lo necesario automáticamente)

### 3.3 Select UI Theme

- Elige el tema que prefieras (Darcula recomendado)

### 3.4 Verify Settings

Revisa que se instalarán:
- Android SDK
- Android SDK Platform
- Android Virtual Device

### 3.5 License Agreement

- Acepta todas las licencias (android-sdk-license, etc.)
- Haz clic en **Finish**

### 3.6 Descarga de componentes

Espera a que se descarguen todos los componentes (puede tardar 10-30 min según conexión).

---

## Paso 4: Configurar SDK

### Acceder a SDK Manager

1. En la pantalla de bienvenida: **More Actions → SDK Manager**
2. O si tienes un proyecto abierto: **Tools → SDK Manager**

### SDK Platforms

Instala al menos:

| Plataforma | API Level | Notas |
|------------|-----------|-------|
| Android 14 (UpsideDownCake) | 34 | Principal para el curso |
| Android 13 (Tiramisu) | 33 | Compatibilidad |

### SDK Tools

En la pestaña **SDK Tools**, asegúrate de tener:

- ✅ Android SDK Build-Tools 34
- ✅ Android SDK Platform-Tools
- ✅ Android Emulator
- ✅ Intel x86 Emulator Accelerator (HAXM) - Solo Windows/Mac Intel
- ✅ Google Play services (opcional pero recomendado)

Haz clic en **Apply** y acepta las licencias.

---

## Paso 5: Configurar emulador

### Crear un AVD (Android Virtual Device)

1. En pantalla de bienvenida: **More Actions → Virtual Device Manager**
2. O: **Tools → Device Manager**
3. Clic en **Create device**

### Seleccionar hardware

1. Categoría: **Phone**
2. Dispositivo recomendado: **Pixel 7** o **Pixel 6**
3. Clic en **Next**

### Seleccionar imagen del sistema

1. Pestaña **Recommended**
2. Descarga **UpsideDownCake** (API 34) - Clic en el icono de descarga
3. Una vez descargado, selecciónalo
4. Clic en **Next**

### Configurar AVD

1. Nombre: deja el por defecto o pon algo descriptivo
2. **Startup orientation:** Portrait
3. **Advanced Settings** (opcional):
   - RAM: 2048 MB (o más si tu PC aguanta)
   - VM heap: 512 MB
4. Clic en **Finish**

### Probar el emulador

1. En Device Manager, clic en ▶️ junto al dispositivo creado
2. Espera a que arranque (primera vez tarda más)
3. Deberías ver la pantalla de inicio de Android

---

## Paso 6: Verificar instalación

### Abrir un proyecto del curso

1. **File → Open**
2. Navega a:
   ```
   cursos/Curso_Android_PMDM_2DAM/projects/todo-compose/starter
   ```
3. Haz clic en **OK**
4. Espera al **Gradle Sync** (primera vez puede tardar 5-10 min)

### Ejecutar el proyecto

1. Selecciona el emulador en el desplegable de dispositivos
2. Clic en ▶️ **Run 'app'**
3. Espera a que compile y se instale
4. La app debería abrirse en el emulador

### Verificación exitosa

Si ves la app ejecutándose en el emulador, ¡instalación completada! ✅

---

## Problemas comunes

### Gradle Sync failed

Ver [04-solucion-problemas.md](04-solucion-problemas.md#gradle-sync-failed)

### SDK not found

1. **File → Project Structure → SDK Location**
2. Verifica que apunta a tu SDK (normalmente en `~/Android/Sdk` o `C:\Users\TU_USUARIO\AppData\Local\Android\Sdk`)

### Emulador muy lento

1. Verifica que tienes virtualización habilitada en BIOS
2. Usa imágenes x86_64, no ARM
3. Asigna más RAM al emulador
4. Cierra otras aplicaciones pesadas

### "HAXM is not installed"

**Windows:**
1. SDK Manager → SDK Tools
2. Instala **Intel x86 Emulator Accelerator (HAXM)**
3. Si falla, ejecuta el instalador manualmente:
   ```
   %LOCALAPPDATA%\Android\Sdk\extras\intel\Hardware_Accelerated_Execution_Manager\intelhaxm-android.exe
   ```

**Linux (usa KVM en lugar de HAXM):**
```bash
sudo apt install qemu-kvm
sudo adduser $USER kvm
```

---

## Configuración adicional recomendada

### Aumentar memoria de Android Studio

**Help → Edit Custom VM Options:**

```
-Xmx4096m
-XX:ReservedCodeCacheSize=512m
```

### Plugins útiles (opcionales)

1. **File → Settings → Plugins**
2. Busca e instala:
   - **Rainbow Brackets** - Colorea paréntesis
   - **Key Promoter X** - Aprende atajos de teclado
   - **.ignore** - Mejor soporte para .gitignore

### Atajos de teclado esenciales

| Acción | Windows/Linux | Mac |
|--------|---------------|-----|
| Ejecutar | Shift+F10 | Ctrl+R |
| Buscar archivo | Ctrl+Shift+N | Cmd+Shift+O |
| Buscar en todo | Double Shift | Double Shift |
| Reformatear código | Ctrl+Alt+L | Cmd+Option+L |
| Generar código | Alt+Insert | Cmd+N |
| Ir a definición | Ctrl+B | Cmd+B |

---

## Siguiente paso

→ [02-flujo-trabajo-git-y-entregas.md](02-flujo-trabajo-git-y-entregas.md)
