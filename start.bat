@echo off
:: ============================================================
::  NETPOLIX - Iniciar backend y frontend juntos
::  Usalo desde la raiz del proyecto: C:\...\NETPOLIX\
:: ============================================================

set ROOT=%~dp0
set BACKEND=%ROOT%backend
set FRONTEND=%ROOT%frontend
set VENV=%ROOT%venv\Scripts\activate.bat

echo.
echo  ==========================================
echo   NETPOLIX - Levantando servidores...
echo  ==========================================
echo.

:: --- Verificar que el venv existe ---
if not exist "%ROOT%venv\Scripts\activate.bat" (
    echo [ERROR] No se encontro el venv en: %ROOT%venv
    echo         Crea el entorno con: python -m venv venv
    pause
    exit /b 1
)

:: --- Verificar que existe el .env ---
if not exist "%BACKEND%\.env" (
    echo [ERROR] No se encontro el archivo .env en: %BACKEND%
    echo         Copia .env.example a .env y completa los valores.
    pause
    exit /b 1
)

:: --- Backend: uvicorn desde backend/ con el venv de la raiz ---
echo [1/2] Iniciando Backend en http://127.0.0.1:8000 ...
start "NETPOLIX - Backend" cmd /k "cd /d %BACKEND% && call %VENV% && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

:: Esperar 2 segundos para que el backend arranque primero
timeout /t 2 /nobreak >nul

:: --- Frontend ---
echo [2/2] Iniciando Frontend...

:: Detectar si es un proyecto Node (tiene package.json) o HTML estatico
if exist "%FRONTEND%\package.json" (
    echo      Detectado proyecto Node.js, corriendo npm run dev...
    start "NETPOLIX - Frontend" cmd /k "cd /d %FRONTEND% && call %VENV% && npm run dev"
) else (
    echo      Detectado frontend estatico, abriendo en el navegador...
    start "" "%FRONTEND%\index.html"
)

echo.
echo  ==========================================
echo   Servidores iniciados!
echo   Backend:  http://127.0.0.1:8000
echo   Docs API: http://127.0.0.1:8000/docs
echo  ==========================================
echo.
echo  Cierra las ventanas de terminal para detener los servidores.
echo.
pause
