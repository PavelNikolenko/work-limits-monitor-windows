$ErrorActionPreference = "Stop"

$AppName = "WorkLimitsMonitor"
$InstallDir = Join-Path $env:LOCALAPPDATA $AppName
$Desktop = [Environment]::GetFolderPath("Desktop")
$Startup = [Environment]::GetFolderPath("Startup")

Remove-Item (Join-Path $Desktop "Work limits.lnk") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $Startup "Work Limits Monitor.lnk") -Force -ErrorAction SilentlyContinue
Remove-Item $InstallDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Work Limits Monitor removed."
