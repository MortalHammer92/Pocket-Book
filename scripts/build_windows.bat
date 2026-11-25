@echo off
title Fabrication de Pocket Book / Building Pocket Book
cd /d "%~dp0\.."

rem Fabrique « PocketBook-Setup-Windows.exe » sur CE PC (il faut Python 3.10+).
rem Builds the Windows installer on THIS PC (Python 3.10+ required).
rem Le plus simple reste de télécharger la version déjà prête dans les Releases GitHub.

set PY=py
py -c "import sys" >nul 2>nul
if not errorlevel 1 goto python_ok
set PY=python
python -c "import sys" >nul 2>nul
if not errorlevel 1 goto python_ok
where uv >nul 2>nul
if not errorlevel 1 goto python_ok
echo.
echo Python est introuvable. / Python not found.
echo Ce script sert a FABRIQUER le programme. Pour simplement l'installer,
echo telechargez PocketBook-Setup-Windows.exe dans les Releases GitHub.
pause
exit /b 1
:python_ok

set VPY=.venv\Scripts\python.exe
if exist "%VPY%" goto venv_ok
echo [1/3] Environnement Python dedie / Build environment...
where uv >nul 2>nul && uv venv --seed .venv
if not exist "%VPY%" %PY% -m venv .venv
if not exist "%VPY%" ( echo Echec .venv & pause & exit /b 1 )
:venv_ok

"%VPY%" -c "import tkinter" 2>nul
if errorlevel 1 ( echo Tkinter manque : installez Python depuis python.org & pause & exit /b 1 )

echo [2/3] PyInstaller...
"%VPY%" -m pip install --upgrade pyinstaller
"%VPY%" -m PyInstaller --version >nul 2>nul
if not errorlevel 1 goto build
where uv >nul 2>nul && uv pip install --python "%VPY%" --upgrade pyinstaller
"%VPY%" -m PyInstaller --version >nul 2>nul
if errorlevel 1 ( echo Echec PyInstaller & pause & exit /b 1 )

:build
echo [3/3] Fabrication / Building...
"%VPY%" -m PyInstaller --noconfirm --clean --onefile --windowed --name "Pocket Book" --icon assets\pocketbook.ico --add-data "assets\pocketbook.ico;." --add-data "assets\pocketbook.png;." pocket_book.py
if errorlevel 1 ( echo Echec de la fabrication & pause & exit /b 1 )
if not exist release mkdir release
copy /y "dist\Pocket Book.exe" "release\PocketBook-Setup-Windows.exe" >nul
echo.
echo Termine / Done : release\PocketBook-Setup-Windows.exe
explorer release
pause
