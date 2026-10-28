@echo off
setlocal
title Math Playground Wiki
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
    py -3 -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
    if not errorlevel 1 (
        py -3 "%~dp0tools\serve_wiki.py" --open
        if errorlevel 1 pause
        exit /b
    )
)
where python >nul 2>&1
if not errorlevel 1 (
    python -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
    if not errorlevel 1 (
        python "%~dp0tools\serve_wiki.py" --open
        if errorlevel 1 pause
        exit /b
    )
)
echo Python 3.10 or newer is required. Install Python and try again.
pause
exit /b 1
