@echo off
set BIN_DIR=bin
set ALT_BIN=BIN_DIR
set OUT_JAR=proyecto-final.jar
set MAIN_CLASS=com.curso.proyectofinal.Application

set SRC_DIR=%BIN_DIR%
if not exist "%SRC_DIR%\com\curso\proyectofinal\Application.class" (
  if exist "%ALT_BIN%\com\curso\proyectofinal\Application.class" (
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
