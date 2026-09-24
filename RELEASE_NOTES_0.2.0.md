# Work Limits Monitor 0.2.0 - Luna Reserve support

A small update born from actual use.

After I exhausted my main allowance and switched to Luna Reserve, I realized the little monitor I had just released had an obvious blind spot: it could show the standard 5-hour and weekly limits, but not the reserve I was now actually watching.

So I made a quick second pass and added:

- a separate Luna Reserve progress bar;
- a Luna Reserve reset countdown;
- automatic window-height adjustment so the new row is never clipped;
- vertical resizing while keeping the compact fixed-width layout.

One important detail: the Luna Reserve bar shows the state of the reserve pool exposed by the local Codex service. It should not be interpreted as proof that a particular task is currently running on Luna.

I am sharing the update with the community in case it saves someone else a few extra trips to the usage page.

This remains an unofficial utility. It only reads local rate-limit information, does not launch Work tasks, does not send prompts, does not spend reset credits, and does not upload telemetry.

Version: 0.2.0
Date: 2026-09-24
