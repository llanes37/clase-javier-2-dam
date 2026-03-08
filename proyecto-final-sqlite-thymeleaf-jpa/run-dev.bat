@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM * Arranque rapido para clase (Windows).
REM ? Objetivo: que el alumno ejecute esto y tenga la app corriendo sin configurar Maven global.
REM ! Si JAVA_HOME no esta definido, intentamos inferirlo a partir de `where java`.

cd /d "%~dp0"

if not exist "mvnw.cmd" (
  echo [ERROR] No se encuentra mvnw.cmd en la carpeta del proyecto.
  echo Abre esta carpeta en VS Code o ejecuta el .bat desde aqui.
  exit /b 1
)

if "%JAVA_HOME%"=="" (
  for /f "delims=" %%J in ('where java 2^>nul') do (
    set "JAVA_EXE=%%J"
    goto :foundjava
  )
)

:foundjava
if "%JAVA_HOME%"=="" (
  if not "%JAVA_EXE%"=="" (
    for %%P in ("%JAVA_EXE%") do set "JAVA_BIN=%%~dpP"
    REM JAVA_BIN = ...\bin\  -> JAVA_HOME = parent of bin
    for %%P in ("!JAVA_BIN!\..") do set "JAVA_HOME=%%~fP"
  )
)

if "%JAVA_HOME%"=="" (
  echo [ERROR] JAVA_HOME no esta definido y no he podido inferirlo.
  echo Solucion:
  echo - Instala un JDK (17+) y define JAVA_HOME apuntando a su carpeta raiz.
  echo - Luego vuelve a ejecutar run-dev.bat
  exit /b 1
)

echo [INFO] JAVA_HOME=%JAVA_HOME%
echo [INFO] Arrancando Spring Boot...
call mvnw.cmd spring-boot:run
