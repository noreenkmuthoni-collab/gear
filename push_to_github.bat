@echo off
REM Batch script to push code to GitHub
REM Repository: https://github.com/noreenkmuthoni-collab/gear.git

echo.
echo ========================================
echo  Push to GitHub - Cold Email Automation
echo ========================================
echo.
echo Repository: https://github.com/noreenkmuthoni-collab/gear.git
echo.

REM Check if git is available
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    echo Or use GitHub Desktop: https://desktop.github.com/
    pause
    exit /b 1
)

echo Git found!
echo.

REM Initialize git if not already initialized
if not exist .git (
    echo Initializing Git repository...
    git init
) else (
    echo Git repository already initialized
)

echo.
echo Adding files...
git add .

echo.
echo Committing changes...
git commit -m "Initial commit: Cold Email Automation AI - Full working system with YT/IG/TikTok channel collection, AI analysis, lead collection, and email automation"

echo.
echo Configuring remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/noreenkmuthoni-collab/gear.git

echo.
echo Setting main branch...
git branch -M main

echo.
echo Pushing to GitHub...
echo You may be prompted for credentials...
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS! Code pushed to GitHub
    echo ========================================
    echo Repository: https://github.com/noreenkmuthoni-collab/gear
    echo.
) else (
    echo.
    echo ========================================
    echo  ERROR: Push failed
    echo ========================================
    echo Check your credentials and try again.
    echo You may need to authenticate with GitHub.
    echo.
)

pause

