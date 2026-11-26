@echo off
title Building Pocket Book
cd /d "%~dp0\.."

rem Builds the Windows installer on THIS PC (Python 3.10+ required).
rem The easiest way is still to download the ready-made version from GitHub Releases.

set PY=py
py -c "import sys" >nul 2>nul
if not errorlevel 1 goto python_ok
set PY=python
python -c "import sys" >nul 2>nul
if not errorlevel 1 goto python_ok
where uv >nul 2>nul
if not errorlevel 1 goto python_ok
echo.
echo Python not found.
echo This script BUILDS the program. To simply install it,
echo download PocketBook-Setup-Windows.exe from GitHub Releases.
pause
exit /b 1
:python_ok

set VPY=.venv\Scripts\python.exe
if exist "%VPY%" goto venv_ok
echo [1/3] Build environment...
where uv >nul 2>nul && uv venv --seed .venv
if not exist "%VPY%" %PY% -m venv .venv
if not exist "%VPY%" ( echo Could not create .venv & pause & exit /b 1 )
:venv_ok

"%VPY%" -c "import tkinter" 2>nul
if errorlevel 1 ( echo Tkinter is missing: install Python from python.org & pause & exit /b 1 )

echo [2/3] PyInstaller...
"%VPY%" -m pip install --upgrade pyinstaller
"%VPY%" -m PyInstaller --version >nul 2>nul
if not errorlevel 1 goto build
where uv >nul 2>nul && uv pip install --python "%VPY%" --upgrade pyinstaller
"%VPY%" -m PyInstaller --version >nul 2>nul
if errorlevel 1 ( echo PyInstaller could not be installed & pause & exit /b 1 )

:build
echo [3/3] Building...
"%VPY%" -m PyInstaller --noconfirm --clean --onefile --windowed --name "Pocket Book" --icon assets\pocketbook.ico --add-data "assets\pocketbook.ico;." --add-data "assets\pocketbook.png;." pocket_book.py
if errorlevel 1 ( echo The build failed & pause & exit /b 1 )
if not exist release mkdir release
copy /y "dist\Pocket Book.exe" "release\PocketBook-Setup-Windows.exe" >nul
echo.
echo Done: release\PocketBook-Setup-Windows.exe
explorer release
pause
