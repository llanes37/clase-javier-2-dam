@echo off
setlocal EnableDelayedExpansion
set SRC_DIR=src
set BIN_DIR=bin
set LIB_DIR=lib

if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo Buscando fuentes...
if exist sources.txt del sources.txt >nul 2>&1
for /R "%SRC_DIR%" %%f in (*.java) do (
  set P=%%f
  set P=!P:\=/!
  echo "!P!" >> sources.txt
)
for /f %%A in ('type sources.txt ^| find /c /v ""') do set COUNT=%%A
if "%COUNT%"=="0" (
  echo No se encontraron archivos .java en %SRC_DIR%
  del sources.txt
  exit /b 1
)

echo Compilando %COUNT% fuentes...
javac -encoding UTF-8 -cp "%BIN_DIR%;%LIB_DIR%/*" -d "%BIN_DIR" @sources.txt
if errorlevel 1 (
  echo Error de compilacion
  del sources.txt
  exit /b 1
)
del sources.txt

echo Compilacion completada.
endlocal
