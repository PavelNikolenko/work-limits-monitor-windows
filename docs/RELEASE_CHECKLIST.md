# Release checklist

## Automated checks

- [x] Python normalization unit test passes
- [x] Windows installer smoke test passes
- [x] Installer creates application files
- [x] Installer creates desktop shortcut
- [x] Uninstaller removes installed files and shortcut

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


Automated Windows smoke test passed in GitHub Actions on 2026-09-23.
