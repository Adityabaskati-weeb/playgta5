@echo off
cd /d "%~dp0"
if not exist "runtime\python.exe" (
    echo Bundled runtime is missing. Extract the entire ZIP before launching.
    pause
    exit /b 1
)
"runtime\python.exe" "serve_local.py" --open %*
set "server_exit=%ERRORLEVEL%"
if not "%server_exit%"=="0" (
    echo.
    echo The server could not start. Check the error above.
    pause
)
exit /b %server_exit%
