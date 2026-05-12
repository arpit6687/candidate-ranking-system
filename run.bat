@echo off
echo ==============================================
echo Candidate Ranking System Setup & Run
echo ==============================================

if not exist venv (
    echo [1/3] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/3] Virtual environment found.
)

echo [2/3] Activating environment...
call venv\Scripts\activate.bat

echo [3/3] Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo ==============================================
echo Starting Server...
echo The app will be available at http://127.0.0.1:5000
echo ==============================================
python app.py
