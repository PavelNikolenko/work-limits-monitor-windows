#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import queue
import shutil
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path

APP_NAME = "work_limits_monitor"
APP_TITLE = "Work Limits Monitor"
APP_VERSION = "0.1.0"
SCHEMA_VERSION = "work-limits/0.1"


class WorkUsageError(RuntimeError):
    pass


def _iso(ts):
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(int(ts)).astimezone().isoformat(timespec="seconds")
    except Exception:
        return None


def _left(used):
    if used is None:
        return None
    try:
        value = max(0.0, min(100.0, 100.0 - float(used)))
        return int(value) if value.is_integer() else round(value, 2)
    except Exception:
        return None


def _window(obj):
    if not isinstance(obj, dict):
        return None
    used = obj.get("usedPercent")
    return {
        "used_percent": used,
        "left_percent": _left(used),
        "window_minutes": obj.get("windowDurationMins"),
        "resets_at_unix": obj.get("resetsAt"),
        "resets_at_local": _iso(obj.get("resetsAt")),
    }


def normalize(payload):
    result = payload.get("result")
    if not isinstance(result, dict):
        raise WorkUsageError("Codex App Server returned no result object.")

    rate_limits = result.get("rateLimits")
    if not isinstance(rate_limits, dict):
        raise WorkUsageError("Codex App Server returned no rateLimits object.")

    reset_credits = result.get("rateLimitResetCredits") or {}

    return {
        "schema_version": SCHEMA_VERSION,
        "observed_at_local": datetime.now().astimezone().isoformat(timespec="seconds"),
        "ordinary_usage_allowed": result.get("ordinaryUsageAllowed"),
        "plan_type": rate_limits.get("planType"),
        "rate_limit_reached_type": rate_limits.get("rateLimitReachedType"),
        "five_hour": _window(rate_limits.get("primary")),
        "weekly": _window(rate_limits.get("secondary")),
        "reset_credits_available": (
            reset_credits.get("availableCount")
            if isinstance(reset_credits, dict)
            else None
        ),
    }


def _codex_command():
    codex = shutil.which("codex")
    if not codex:
        raise WorkUsageError(
            "Codex CLI was not found in PATH. Install/login to Codex CLI first."
        )

    if os.name == "nt" and Path(codex).suffix.lower() in {".cmd", ".bat"}:
        return (
            subprocess.list2cmdline([codex, "app-server", "--listen", "stdio://"]),
            True,
        )
    return [codex, "app-server", "--listen", "stdio://"], False


def _reader(stream, q, tag):
    try:
        for line in iter(stream.readline, ""):
            q.put((tag, line.rstrip("\r\n")))
    finally:
        q.put((tag, None))


def _send(proc, obj):
    if proc.stdin is None:
        raise WorkUsageError("Codex App Server stdin is unavailable.")
    proc.stdin.write(json.dumps(obj, ensure_ascii=False) + "\n")
    proc.stdin.flush()


def _wait(q, request_id, timeout):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            tag, line = q.get(timeout=max(0.05, deadline - time.monotonic()))
        except queue.Empty:
            break

        if line is None or tag != "stdout":
            continue

        try:
            msg = json.loads(line)
        except Exception:
            continue

        if msg.get("id") != request_id:
            continue

        if "error" in msg:
            raise WorkUsageError(str(msg["error"]))
        return msg

    raise WorkUsageError(f"Timed out waiting for Codex response id={request_id}")


def get_usage(timeout=15.0):
    command, shell = _codex_command()

    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        shell=shell,
    )

    q = queue.Queue()
    assert proc.stdout is not None and proc.stderr is not None

    for stream, tag in ((proc.stdout, "stdout"), (proc.stderr, "stderr")):
        threading.Thread(target=_reader, args=(stream, q, tag), daemon=True).start()

    try:
        _send(
            proc,
            {
                "method": "initialize",
                "id": 1,
                "params": {
                    "clientInfo": {
                        "name": APP_NAME,
                        "title": APP_TITLE,
                        "version": APP_VERSION,
                    }
                },
            },
        )
        _wait(q, 1, timeout)
        _send(proc, {"method": "initialized", "params": {}})
        _send(proc, {"method": "account/rateLimits/read", "id": 2})
        return normalize(_wait(q, 2, timeout))
    finally:
        try:
            if proc.stdin:
                proc.stdin.close()
        except Exception:
            pass
        if proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=3)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
