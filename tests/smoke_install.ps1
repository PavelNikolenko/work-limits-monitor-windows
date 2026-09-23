$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path $PSScriptRoot -Parent
$FakeBin = Join-Path $env:RUNNER_TEMP "work-limits-fake-bin"
$InstallDir = Join-Path $env:LOCALAPPDATA "WorkLimitsMonitor"

New-Item -ItemType Directory -Force -Path $FakeBin | Out-Null

$FakeCodex = Join-Path $FakeBin "codex.cmd"
$FakeCodexContent = "@echo off" + [Environment]::NewLine + "exit /b 0" + [Environment]::NewLine
Set-Content -Path $FakeCodex -Encoding ASCII -Value $FakeCodexContent

$env:PATH = "$FakeBin;$env:PATH"
$env:WLM_SKIP_LAUNCH = "1"

Write-Host "Running installer smoke test..."
& (Join-Path $RepoRoot "install\install.ps1")

$Expected = @(
    (Join-Path $InstallDir "WorkLimitMonitor.py"),
    (Join-Path $InstallDir "WorkUsage.py")
)

foreach ($Path in $Expected) {
    if (-not (Test-Path $Path)) {
        throw "Expected installed file not found: $Path"
    }
}

$Desktop = [Environment]::GetFolderPath("Desktop")
$Shortcut = Join-Path $Desktop "Work Limits Monitor.lnk"
if (-not (Test-Path $Shortcut)) {
    throw "Desktop shortcut was not created: $Shortcut"
}

Write-Host "Running uninstaller smoke test..."
& (Join-Path $RepoRoot "install\uninstall.ps1")

if (Test-Path $InstallDir) {
    throw "Install directory still exists after uninstall: $InstallDir"
}

if (Test-Path $Shortcut) {
    throw "Desktop shortcut still exists after uninstall: $Shortcut"
}

Write-Host "Windows installer smoke test: PASS"
