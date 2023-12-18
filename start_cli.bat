@echo off

if not exist venv (
    echo Creating venv...
    python -m venv venv
    call venv\Scripts\activate
    echo Installing dependencies...
    python.exe -m pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error happens. Deleting venv...
        rmdir /s /q venv
        exit
    )
) else (
    call venv\Scripts\activate
)
python3 start_cli.py
deactivate