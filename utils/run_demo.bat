@echo off
echo 🎵 Spotify Mood Analyzer Demo
echo =====================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting demo server...
echo Demo will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause 