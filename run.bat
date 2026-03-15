@echo off
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please download and install Python 3 from python.org
    echo Make sure to check "Add Python to PATH" during installation!
    pause
    exit /b
)

echo.
echo Installing required libraries (Pillow, customtkinter) using pip...
pip install Pillow customtkinter

echo.
echo Starting the program...
python boot_creator.py

pause
