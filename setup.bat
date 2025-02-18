@echo off

REM Are you here python ?
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python is not installed :c
    echo [INFO] Install Python here : https://www.python.org/
    pause
    exit /b 1
)

REM Are you here pip ?
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Pip is not installed :c
    echo [INFO] Install pip with this command in ur cmd : 'python -m ensurepip'
    pause
    exit /b 1
)

REM Welcome to my dungeon !
echo ========================================
echo                Setup
echo ========================================

echo [INFO] Insatllation of keyboard ...
python -m pip install keyboard
if %errorlevel% equ 0 (
    echo [SUCCESS] Keyboard was installed with success !
) else (
    echo [ERROR] Keyboard can't be installed :c
)

REM Installation de tkinter
echo [INFO] Installation of tkinter ...
python -m pip install tk
if %errorlevel% equ 0 (
    echo [SUCCESS] Tkinter was installed with success !
) else (
    echo [ERROR] Tkinter can't be installed :c
)

REM Dungeon Finished !
echo ========================================
echo              Finished !
echo ========================================

pause