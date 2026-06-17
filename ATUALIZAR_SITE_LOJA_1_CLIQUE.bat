@echo off
setlocal
title Palmon Survival - Atualizar Loja
cd /d "%~dp0"
echo Palmon Survival - atualizacao 1 clique da loja
echo.
echo Onde colocar ZIP:
echo %~dp0COLOQUE_O_ZIP_AQUI
echo.
echo Voce tambem pode arrastar o ZIP em cima deste BAT.
echo.
if "%~1"=="" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0update_palmon_shop_site.ps1"
) else (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0update_palmon_shop_site.ps1" -ZipPath "%~1"
)
set EXITCODE=%ERRORLEVEL%
echo.
if "%EXITCODE%"=="0" (
  echo Concluido com sucesso.
) else (
  echo Falhou. Veja o log na pasta logs.
)
echo.
pause
exit /b %EXITCODE%
