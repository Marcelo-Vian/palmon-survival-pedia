@echo off
setlocal
cd /d "%~dp0"
echo Palmon Survival - atualizacao 1 clique da loja
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0update_palmon_shop_site.ps1"
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
