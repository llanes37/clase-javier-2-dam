@echo off
set BIN_DIR=bin
set ALT_BIN=BIN_DIR
set OUT_JAR=proyecto-final-basico.jar
set MAIN_CLASS=com.curso.proyectobasico.Application

set SRC_DIR=%BIN_DIR%
if not exist "%SRC_DIR%\com\curso\proyectobasico\Application.class" (
  if exist "%ALT_BIN%\com\curso\proyectobasico\Application.class" (
    set SRC_DIR=%ALT_BIN%
  ) else (
    echo No se encontraron clases compiladas. Ejecuta build.bat primero.
    exit /b 1
  )
)

echo Creando manifest temporal...
echo Main-Class: %MAIN_CLASS% > manifest.txt
echo Class-Path: . >> manifest.txt

echo Empaquetando jar desde %SRC_DIR% ...
jar cfm "%OUT_JAR%" manifest.txt -C "%SRC_DIR%" .
del manifest.txt

echo Jar creado: %OUT_JAR%

