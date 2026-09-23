# Work Limits Monitor v0.1.0

First stable public release of Work Limits Monitor for Windows.

## What it does

- shows the remaining 5-hour Codex allowance;
- shows the remaining weekly Codex allowance;
- shows countdowns to both reset times;
- shows reset credits when exposed by the local Codex service;
- shows the current plan type;
- refreshes automatically every 30 seconds;
- can stay always on top;
- installs a desktop shortcut and optional Windows Startup entry.

## Privacy

The application reads rate-limit state from the locally authenticated Codex CLI session.

It does not:

- send prompts;
- launch ChatGPT Work tasks;
- modify conversations;
- upload telemetry;
- store OpenAI credentials;
- spend reset credits.

## Requirements

- Windows 10 or Windows 11
- Python 3.10+
- Codex CLI installed and available in PATH
- authenticated Codex CLI session

## Installation

From PowerShell in the repository directory:

```powershell
.\install\install.ps1
```

## Important limitation

Work Limits Monitor uses the local Codex app-server method `account/rateLimits/read`. This is an unofficial interface and may change in a future Codex release.
