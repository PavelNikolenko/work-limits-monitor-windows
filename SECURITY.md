# Security Policy

## Supported version

The current release candidate is `0.1.0-rc1`.

## Reporting a vulnerability

Please open a private GitHub security advisory for the repository if available.

Do not include access tokens, cookies, account exports, conversation data, local profile data, or other secrets in a public issue.

## Security model

Work Limits Monitor:

- does not ask for an OpenAI API key;
- does not store Codex authentication credentials;
- does not send telemetry;
- does not modify Codex or ChatGPT data;
- launches the locally installed `codex app-server` process only to read rate-limit state.

Users should review the source before running PowerShell scripts downloaded from the Internet.
