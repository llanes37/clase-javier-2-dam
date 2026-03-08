@echo off
set BIN_DIR=bin
set ALT_BIN=BIN_DIR
set LIB_DIR=lib

REM Usa bin si existe la clase, si no intenta ALT_BIN (compatibilidad)
set MAIN_CLASS=com.curso.proyectofinal.Application
set CP="%BIN_DIR%;%ALT_BIN%;%LIB_DIR%/*"

java -cp %CP% %MAIN_CLASS% %*
