@echo off
setlocal enabledelayedexpansion

:: Navigate to repository directory where push.bat is located
cd /d "%~dp0"

echo ========================================================
echo   Auto Git Add, Commit and Push - Interval: 1 minute
echo   Target: Active / Current Branch
echo   Press Ctrl+C at any time to stop this script.
echo ========================================================
echo.

:loop
:: Detect current active branch dynamically
set "BRANCH="
for /f "tokens=*" %%b in ('git branch --show-current') do set "BRANCH=%%b"

if "%BRANCH%"=="" (
    echo [%date% %time%] Warning: Could not detect active branch. Detached HEAD?
    goto wait
)

echo [%date% %time%] Active branch: %BRANCH%
echo [%date% %time%] Checking for changes...

:: Stage all changes
git add .

:: Check if there are staged changes to commit
git diff --cached --quiet
if errorlevel 1 (
    echo [%date% %time%] Changes detected. Committing...
    git commit -m "Auto-commit: %date% %time%"

    echo [%date% %time%] Pushing changes to origin/%BRANCH%...
    git push -u origin %BRANCH%
    if errorlevel 1 (
        echo [%date% %time%] Push failed. Check your network connection or permissions.
    ) else (
        echo [%date% %time%] Push to origin/%BRANCH% completed successfully.
    )
) else (
    echo [%date% %time%] No changes to commit.
)

:wait
echo.
timeout /t 60 2>nul
if errorlevel 1 (
    for /l %%i in (60,-1,1) do (
        <nul set /p "=Waiting %%i seconds... "
        ping 127.0.0.1 -n 2 >nul
        echo.
    )
)
echo.
goto loop