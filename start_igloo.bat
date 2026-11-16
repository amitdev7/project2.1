@echo off
title Igloo Inc. - 3D Local Server
cd /d "%~dp0"
echo ===================================================
echo   Launching Igloo Inc. Offline 3D Experience
echo   Local URL: http://localhost:5502/
echo   Direct IP: http://127.0.0.1:5502/
echo ===================================================
python server.py
pause
