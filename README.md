# Work Limits Monitor for Windows

Unofficial lightweight Windows desktop monitor for Codex rate limits.

[Русская версия](README_RU.md)

> Status: `0.1.0-rc1` release candidate. The code is public and usable, but the standalone public installer should be tested on a clean Windows setup before the first stable release.

## Why this exists

When you use Codex or ChatGPT Work heavily, the practical question is often simple: **how much of the current 5-hour and weekly allowance is left?**

Checking that manually means repeatedly opening the usage/limits page in ChatGPT. Work Limits Monitor keeps those values in a small Windows window that can stay visible while you work.

It shows:

- remaining 5-hour allowance;
- remaining weekly allowance;
- time until each window resets;
- available reset credits, when exposed by the local Codex service;
- current plan type;
- automatic refresh every 30 seconds.

The app is intentionally small. It does not launch ChatGPT Work tasks, send prompts, modify conversations, or spend reset credits.

## How it works

The application starts the locally installed Codex CLI in app-server mode and reads rate-limit information using:

`account/rateLimits/read`

The UI displays the normalized values returned by that local service.

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

The application does not contain account IDs, conversation IDs, email addresses, local usernames, or fixed user paths.

It reads rate-limit data from the locally authenticated Codex CLI session. It does not upload telemetry or usage history anywhere.

## Limitations

- This project reads an internal/local Codex app-server interface. It can break if that interface changes.
- It reports the rate-limit values exposed by Codex. It does not calculate token counts.
- "5-hour" and "weekly" values are percentages of the corresponding rate-limit windows, not token balances.

## Security

See [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](LICENSE).

## Support

If this utility saves you repeated trips to the ChatGPT usage page, starring the repository helps other users find it.

A voluntary support link can be added later.
