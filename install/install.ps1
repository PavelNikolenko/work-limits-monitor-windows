$ErrorActionPreference = "Stop"

$AppName = "WorkLimitsMonitor"
$InstallDir = Join-Path $env:LOCALAPPDATA $AppName
$SourceDir = Join-Path $PSScriptRoot "..\src"

Write-Host "Work Limits Monitor 0.2.0"
Write-Host "Unofficial Windows monitor for Codex rate limits."

$Python = (Get-Command python.exe -ErrorAction SilentlyContinue).Source
$PythonW = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
$Codex = (Get-Command codex -ErrorAction SilentlyContinue).Source

if (-not $Python) { throw "Python 3 was not found in PATH." }
if (-not $PythonW) { $PythonW = $Python }
if (-not $Codex) { throw "Codex CLI was not found in PATH. Install and sign in to Codex CLI first." }

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item (Join-Path $SourceDir "WorkLimitMonitor.py") $InstallDir -Force
Copy-Item (Join-Path $SourceDir "WorkUsage.py") $InstallDir -Force

& $Python -m py_compile (Join-Path $InstallDir "WorkLimitMonitor.py")
if ($LASTEXITCODE -ne 0) { throw "WorkLimitMonitor.py syntax check failed." }
& $Python -m py_compile (Join-Path $InstallDir "WorkUsage.py")
if ($LASTEXITCODE -ne 0) { throw "WorkUsage.py syntax check failed." }

$Wsh = New-Object -ComObject WScript.Shell
$Desktop = [Environment]::GetFolderPath("Desktop")
$DesktopLink = Join-Path $Desktop "Work Limits Monitor.lnk"
$Shortcut = $Wsh.CreateShortcut($DesktopLink)
$Shortcut.TargetPath = $PythonW
$Shortcut.Arguments = '"' + (Join-Path $InstallDir "WorkLimitMonitor.py") + '"'
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description = "Work Limits Monitor for Codex rate limits"
$Shortcut.Save()

$Startup = [Environment]::GetFolderPath("Startup")
$StartupLink = Join-Path $Startup "Work Limits Monitor.lnk"
$StartupShortcut = $Wsh.CreateShortcut($StartupLink)
$StartupShortcut.TargetPath = $PythonW
$StartupShortcut.Arguments = '"' + (Join-Path $InstallDir "WorkLimitMonitor.py") + '"'
$StartupShortcut.WorkingDirectory = $InstallDir
$StartupShortcut.Description = "Work / Codex rate-limit monitor"
$StartupShortcut.Save()

Write-Host "Installed to:"
Write-Host "  $InstallDir"
Write-Host "Desktop shortcut:"
Write-Host "  $DesktopLink"
Write-Host "Startup shortcut:"
Write-Host "  $StartupLink"
Write-Host ""
if ($env:WLM_SKIP_LAUNCH -eq "1") {
    Write-Host "Launch skipped by WLM_SKIP_LAUNCH=1."
} else {
    Write-Host "Launching..."
    Start-Process -FilePath $PythonW -ArgumentList ('"' + (Join-Path $InstallDir "WorkLimitMonitor.py") + '"') -WorkingDirectory $InstallDir
}
Write-Host "Done."
