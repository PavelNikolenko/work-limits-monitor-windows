#!/usr/bin/env python3
from __future__ import annotations

import json
import queue
import sys
import threading
import time
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import ttk

from WorkUsage import get_usage

APP_VERSION = "0.1.0"
REFRESH_SECONDS = 30

APP_DIR = Path(__file__).resolve().parent
STATE_DIR = Path.home() / ".work-limits-monitor"
STATE_PATH = STATE_DIR / "state.json"


def fmt_percent(value):
    if value is None:
        return "--"
    try:
        value = float(value)
        return f"{int(value)}%" if value.is_integer() else f"{value:.1f}%"
    except Exception:
        return "--"


def fmt_countdown(ts):
    if ts is None:
        return "no data"
    try:
        seconds = max(0, int(float(ts) - time.time()))
    except Exception:
        return "no data"

    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)

    if days:
        return f"{days}d {hours}h {minutes}m"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def clamp(value):
    try:
        return max(0.0, min(100.0, float(value)))
    except Exception:
        return 0.0


class LimitMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Work Limits Monitor")
        self.resizable(False, False)
        self.minsize(360, 0)

        self.messages = queue.Queue()
        self.refresh_in_progress = False
        self.latest_usage = None
        self.topmost_var = tk.BooleanVar(value=True)

        self._load_state()
        self._build_ui()
        self.attributes("-topmost", bool(self.topmost_var.get()))

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._poll_queue)
        self.after(1000, self._tick)
        self.after(250, self.refresh_now)

    def _build_ui(self):
        outer = ttk.Frame(self, padding=12)
        outer.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            outer,
            text="Work / Codex limits",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

        ttk.Label(outer, text="5-hour").grid(row=1, column=0, sticky="w")
        self.five_label = ttk.Label(outer, text="--", font=("Segoe UI", 12, "bold"))
        self.five_label.grid(row=1, column=2, sticky="e")
        self.five_bar = ttk.Progressbar(
            outer, orient="horizontal", length=300, mode="determinate", maximum=100
        )
        self.five_bar.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(3, 2))
        self.five_reset = ttk.Label(outer, text="Reset in: --")
        self.five_reset.grid(row=3, column=0, columnspan=3, sticky="w", pady=(0, 9))

        ttk.Label(outer, text="Weekly").grid(row=4, column=0, sticky="w")
        self.week_label = ttk.Label(outer, text="--", font=("Segoe UI", 12, "bold"))
        self.week_label.grid(row=4, column=2, sticky="e")
        self.week_bar = ttk.Progressbar(
            outer, orient="horizontal", length=300, mode="determinate", maximum=100
        )
        self.week_bar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(3, 2))
        self.week_reset = ttk.Label(outer, text="Reset in: --")
        self.week_reset.grid(row=6, column=0, columnspan=3, sticky="w", pady=(0, 9))

        ttk.Separator(outer, orient="horizontal").grid(
            row=7, column=0, columnspan=3, sticky="ew", pady=(1, 8)
        )

        self.credits_label = ttk.Label(outer, text="Reset credits: --")
        self.credits_label.grid(row=8, column=0, columnspan=3, sticky="w")
        self.plan_label = ttk.Label(outer, text="Plan: --")
        self.plan_label.grid(row=9, column=0, columnspan=3, sticky="w")
        self.updated_label = ttk.Label(outer, text="Updated: --")
        self.updated_label.grid(row=10, column=0, columnspan=3, sticky="w")
        self.status_label = ttk.Label(
            outer, text=f"Auto-refresh: every {REFRESH_SECONDS}s"
        )
        self.status_label.grid(row=11, column=0, columnspan=3, sticky="w", pady=(3, 8))

        ttk.Button(outer, text="Refresh", command=self.refresh_now).grid(
            row=12, column=0, sticky="w"
        )
        ttk.Checkbutton(
            outer,
            text="Always on top",
            variable=self.topmost_var,
            command=self._toggle_topmost,
        ).grid(row=12, column=1, sticky="e", padx=(12, 6))
        ttk.Button(outer, text="Close", command=self._on_close).grid(
            row=12, column=2, sticky="e"
        )

    def _load_state(self):
        try:
            data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            geometry = data.get("geometry")
            if geometry:
                self.geometry(geometry)
            topmost = data.get("topmost")
            if isinstance(topmost, bool):
                self.topmost_var.set(topmost)
        except Exception:
            pass

    def _save_state(self):
        try:
            STATE_DIR.mkdir(parents=True, exist_ok=True)
            STATE_PATH.write_text(
                json.dumps(
                    {
                        "geometry": self.geometry(),
                        "topmost": bool(self.topmost_var.get()),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        except Exception:
            pass

    def _toggle_topmost(self):
        self.attributes("-topmost", bool(self.topmost_var.get()))
        self._save_state()

    def refresh_now(self):
        if self.refresh_in_progress:
            return
        self.refresh_in_progress = True
        self.status_label.configure(text="Refreshing...")
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            self.messages.put(("ok", get_usage(timeout=15.0)))
        except Exception as exc:
            self.messages.put(("error", str(exc)))

    def _poll_queue(self):
        try:
            while True:
                kind, payload = self.messages.get_nowait()
                self.refresh_in_progress = False
                if kind == "ok":
                    self.latest_usage = payload
                    self._apply_usage(payload)
                else:
                    self.status_label.configure(text=f"Error: {payload}")
        except queue.Empty:
            pass
        self.after(150, self._poll_queue)

    def _apply_usage(self, usage):
        five = usage.get("five_hour") or {}
        weekly = usage.get("weekly") or {}

        self.five_label.configure(text=fmt_percent(five.get("left_percent")))
        self.week_label.configure(text=fmt_percent(weekly.get("left_percent")))
        self.five_bar["value"] = clamp(five.get("left_percent"))
        self.week_bar["value"] = clamp(weekly.get("left_percent"))

        self.credits_label.configure(
            text=f"Reset credits: {usage.get('reset_credits_available', '--')}"
        )
        self.plan_label.configure(text=f"Plan: {usage.get('plan_type') or '--'}")

        observed = usage.get("observed_at_local")
        if observed:
            try:
                observed = datetime.fromisoformat(observed).strftime("%H:%M:%S")
            except Exception:
                pass
        self.updated_label.configure(text=f"Updated: {observed or '--'}")
        self.status_label.configure(text=f"Auto-refresh: every {REFRESH_SECONDS}s")
        self._tick()

    def _tick(self):
        if self.latest_usage:
            five = self.latest_usage.get("five_hour") or {}
            weekly = self.latest_usage.get("weekly") or {}
            self.five_reset.configure(
                text=f"Reset in: {fmt_countdown(five.get('resets_at_unix'))}"
            )
            self.week_reset.configure(
                text=f"Reset in: {fmt_countdown(weekly.get('resets_at_unix'))}"
            )
        self.after(1000, self._tick)

    def _on_close(self):
        self._save_state()
        self.destroy()

    def run_auto_refresh(self):
        def schedule():
            if self.winfo_exists():
                self.refresh_now()
                self.after(REFRESH_SECONDS * 1000, schedule)

        self.after(REFRESH_SECONDS * 1000, schedule)


if __name__ == "__main__":
    app = LimitMonitor()
    app.run_auto_refresh()
    app.mainloop()
