@echo off
setlocal
cd /d "%~dp0"
title WildSense Local Website
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3 from https://www.python.org/downloads/windows/
  echo During setup, enable "Add python.exe to PATH".
  pause
  exit /b 1
)
where ollama >nul 2>nul
if errorlevel 1 (
  echo Ollama is not installed. The website and journal can still be reviewed without AI.
  echo To enable local AI, install Ollama from https://ollama.com/download
  start "" "https://ollama.com/download"
  echo After installation, close this window and run start.bat again.
  start "" "http://127.0.0.1:8765"
  python server.py
  pause
  exit /b
)
start "WildSense Website" "http://127.0.0.1:8765"
ollama list | findstr /i "llama3.2:1b" >nul
if errorlevel 1 (
  echo First-time setup: downloading the llama3.2:1b model. This needs internet and disk space.
  ollama pull llama3.2:1b
  if errorlevel 1 echo Model download failed. Check your internet and run: ollama pull llama3.2:1b
)
python server.py
pause
