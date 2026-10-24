@echo off
rem Local preview for the MkDocs site. Keep this file ASCII-only.
cd /d "%~dp0"
echo Starting local preview at http://127.0.0.1:8765/
echo (The browser will open after the server is ready. Press Ctrl+C to stop.)
start "" /b cmd /c "timeout /t 6 /nobreak >nul & start http://127.0.0.1:8765/"
python -m mkdocs serve -a 127.0.0.1:8765
pause
