# Release checklist

## Automated checks

- [ ] Python normalization unit test passes
- [ ] Windows installer smoke test passes
- [ ] Installer creates application files
- [ ] Installer creates desktop shortcut
- [ ] Uninstaller removes installed files and shortcut

## Manual integration check

- [ ] Application opens on Windows
- [ ] 5-hour value matches the ChatGPT/Codex limits page
- [ ] Weekly value matches the ChatGPT/Codex limits page
- [ ] Reset countdowns are plausible
- [ ] Reset credits match when available
- [ ] No personal identifiers are present in the public repository

## Release

- [ ] Update README status from release candidate to stable
- [ ] Update SECURITY.md supported version
- [ ] Publish GitHub Release `v0.1.0`
