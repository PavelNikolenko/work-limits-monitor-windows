# Work Limits Monitor for Windows

[![Windows smoke test](https://github.com/PavelNikolenko/work-limits-monitor-windows/actions/workflows/windows-smoke.yml/badge.svg)](https://github.com/PavelNikolenko/work-limits-monitor-windows/actions/workflows/windows-smoke.yml)

Unofficial lightweight Windows desktop monitor for Codex rate limits.

[Русская версия](README_RU.md)

> Current version: 0.2.0

## Why this exists

When you use Codex or ChatGPT Work heavily, the practical question is simple: how much allowance is left right now?

Work Limits Monitor keeps the available rate-limit windows in a small Windows window that can stay visible while you work.

It shows:

- remaining 5-hour allowance;
- remaining weekly allowance;
- Luna Reserve allowance, when exposed by the local Codex service;
- time until each displayed window resets;
- available reset credits, when exposed;
- current plan type;
- automatic refresh every 30 seconds.

The Luna Reserve row is a reserve-pool indicator. Its presence or remaining percentage does not by itself prove that a specific task is currently running on Luna.

The app is intentionally small. It does not launch ChatGPT Work tasks, send prompts, modify conversations, or spend reset credits.

## What changed in 0.2.0

The update came directly from real use. After the main allowance was exhausted and I moved to Luna Reserve, I realized the monitor had an obvious blind spot: it showed the standard 5-hour and weekly windows, but not the reserve I was actually relying on.

Version 0.2.0 adds a separate Luna Reserve progress bar and reset countdown. It also fixes window sizing so the interface automatically grows when new rows are added and can be resized vertically.

See [RELEASE_NOTES_0.2.0.md](RELEASE_NOTES_0.2.0.md) and [CHANGELOG.md](CHANGELOG.md).

## Interface preview

![Work Limits Monitor interface preview](docs/work-limits-monitor-preview.png)

*Preview of version 0.2.0 with sample values. Actual values and available rows come from your local Codex session.*

## How it works

The application starts the locally installed Codex CLI in app-server mode and reads rate-limit information using:

`account/rateLimits/read`

For Luna Reserve discovery, the request enables the Luna reserve capability exposed by the local service.

This is an unofficial community utility. The Codex app-server interface is not guaranteed to remain stable and may change in future Codex releases.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- Codex CLI installed and available in `PATH`
- an authenticated Codex CLI session

No third-party Python packages are required.

## Install

Download or clone the repository, open PowerShell in the repository folder, then run:

```powershell
cd path\to\work-limits-monitor-windows
.\install\install.ps1
```

The installer:

1. verifies Python and Codex CLI;
2. copies the application to `%LOCALAPPDATA%\WorkLimitsMonitor`;
3. creates a desktop shortcut named `Work Limits Monitor`;
4. adds the app to the current user's Windows Startup folder;
5. launches the monitor.

After installation, PowerShell can be closed.

## Start manually

Use the desktop shortcut, or run:

```bat
start.bat
```

## Uninstall

```powershell
cd path\to\work-limits-monitor-windows
.\install\uninstall.ps1
```

## Privacy

The application does not contain account IDs, conversation IDs, email addresses, local usernames, fixed user paths, or data from any larger private project.

It reads rate-limit data from the locally authenticated Codex CLI session. It does not upload telemetry or usage history anywhere.

## Limitations

- This project reads an internal/local Codex app-server interface. It can break if that interface changes.
- It reports the rate-limit values exposed by Codex. It does not calculate token counts.
- 5-hour, weekly, and Luna Reserve percentages are rate-limit-window values, not token balances.
- The Luna Reserve row shows reserve availability, not active-model routing.

## Security

See [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).

## Support

If this utility saves you repeated trips to the ChatGPT usage page, starring the repository helps other users find it.

You can also support the project with a voluntary tip on Ko-fi:

https://ko-fi.com/pavelnikolenko
