# Changelog

All changes to the Printer Buddy streamer, newest first.

################################2026-11-24 sterling m security/no-v4l-utils################################

## Read a camera's formats directly, no v4l-utils

Checking whether a USB camera can send MJPEG now asks the camera itself (the `VIDIOC_ENUM_FMT` call on its `/dev/video` device, in the machine's own byte order) instead of running `v4l2-ctl`, so the streamer no longer needs the v4l-utils package. *Why:* Printer Buddy is dropping the system packages it installed as root; this was the only thing v4l-utils was used for.

Lines changed:
- `streamer/detect.py` — 12, 18 import `fcntl` and `struct`; 21–23 add `VIDIOC_ENUM_FMT` and `MJPG`; 42–60 `has_mjpeg` reads the formats from the device
- `README.md` — 29–31 drop `v4l2-ctl` from what each tier needs

################################end of entry################################

################################2026-11-20 sterling m streamer################################

## Let Printer Buddy point the mjpg-streamer binaries anywhere

`MJPG_DIR` now reads the `PB_MJPG_DIR` environment variable, falling back to the old `/usr/local/lib/print-buddy-streamer/mjpg-streamer` path. *Why:* Printer Buddy now runs the streamer itself and keeps the binaries in its own folder (no root), so it tells the streamer where they are via that variable; unset, nothing changes.

Lines changed:
- `streamer/backends.py` — 21 read `MJPG_DIR` from `PB_MJPG_DIR` (default unchanged)

################################end of entry################################
