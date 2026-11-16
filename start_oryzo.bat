@echo off
cd /d "%~dp0"
title AMIT AI 1:1 Standalone WebGL / 3D Experience
echo Starting AMIT AI local server on port 5501...
python -u server.py
pause
