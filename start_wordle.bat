@echo off
title Wordle Terminal Game
echo Starting Wordle Terminal Game...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is required to run this game but is not installed.
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Check if colorama is installed
python -c "import colorama" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Colorama package is required but not installed.
    echo Installing colorama...
    pip install colorama
)

REM Run the game
cls
echo Launching Wordle...
python wordle.py

REM Keep the window open after the game ends
echo.
echo Game ended. Press any key to exit.
pause >nul