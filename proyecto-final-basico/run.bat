@echo off
set BIN_DIR=bin
set ALT_BIN=BIN_DIR
set LIB_DIR=lib

set MAIN_CLASS=com.curso.proyectobasico.Application
set CP="%BIN_DIR%;%ALT_BIN%;%LIB_DIR%/*"

java -cp %CP% %MAIN_CLASS% %*

