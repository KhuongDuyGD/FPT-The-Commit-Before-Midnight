@echo off
setlocal
for %%I in ("%~dp0.") do set "GAME_DIR=%%~fI"
set "SDK_DIR=%RENPY_SDK%"
if not defined SDK_DIR set "SDK_DIR=%TEMP%\fpt-commit-rebuild-sdk\renpy-8.5.3-sdk"

if not exist "%SDK_DIR%\renpy.exe" (
    echo Khong tim thay Ren'Py SDK tai: "%SDK_DIR%"
    echo Hay cai Ren'Py 8.5.3+ va dat bien RENPY_SDK tro den thu muc SDK.
    pause
    exit /b 1
)

start "" "%SDK_DIR%\renpy.exe" "%GAME_DIR%"
