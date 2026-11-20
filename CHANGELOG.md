# Changelog

All changes to the Printer Buddy streamer, newest first.

################################2026-11-20 sterling m streamer################################

## Let Printer Buddy point the mjpg-streamer binaries anywhere

`MJPG_DIR` now reads the `PB_MJPG_DIR` environment variable, falling back to the old `/usr/local/lib/print-buddy-streamer/mjpg-streamer` path. *Why:* Printer Buddy now runs the streamer itself and keeps the binaries in its own folder (no root), so it tells the streamer where they are via that variable; unset, nothing changes.

Lines changed:
- `streamer/backends.py` — 21 read `MJPG_DIR` from `PB_MJPG_DIR` (default unchanged)

################################end of entry################################
