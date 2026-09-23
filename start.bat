@echo off
setlocal
set "APP=%LOCALAPPDATA%\WorkLimitsMonitor\WorkLimitMonitor.py"

if not exist "%APP%" (
  echo Work Limits Monitor is not installed.
  echo Run install\install.ps1 first.
  pause
  exit /b 1
)

where pythonw.exe >nul 2>&1
if errorlevel 1 (
  echo pythonw.exe was not found in PATH.
  pause
  exit /b 1
)

start "" pythonw.exe "%APP%"
exit /b 0
