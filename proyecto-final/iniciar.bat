@echo off
setlocal

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

set "JDK_BIN="

if exist "C:\Users\barqu\.vscode\extensions\redhat.java-1.52.0-win32-x64\jre\21.0.9-win32-x86_64\bin\java.exe" set "JDK_BIN=C:\Users\barqu\.vscode\extensions\redhat.java-1.52.0-win32-x64\jre\21.0.9-win32-x86_64\bin"
if not defined JDK_BIN if exist "C:\Users\barqu\.jdks\openjdk-25.0.1\bin\java.exe" set "JDK_BIN=C:\Users\barqu\.jdks\openjdk-25.0.1\bin"
if not defined JDK_BIN if exist "C:\Users\barqu\Desktop\jdk\jdk-20.0.1\bin\java.exe" set "JDK_BIN=C:\Users\barqu\Desktop\jdk\jdk-20.0.1\bin"

if not defined JDK_BIN (
  echo No encuentro un JDK compatible.
  echo Abre VS Code y ejecuta Application.java con el boton Run.
  pause
  exit /b 1
)

set "PATH=%JDK_BIN%;%PATH%"

call build.bat
if errorlevel 1 (
  echo Fallo al compilar.
  pause
  exit /b 1
)

call run.bat
pause

endlocal
