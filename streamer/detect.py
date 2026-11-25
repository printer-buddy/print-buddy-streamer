#LICENSE
#
#Copyright (C) 2026  sterling motuz <Sterling@dexabyte.ca>
#
#for https://github.com/printer-buddy/printer-buddy
#
#SPDX-License-Identifier: AGPL-3.0-only
#
#Additional term (AGPL-3.0 section 7b, keep author credit): keep this header
#
#Additional term (AGPL-3.0 section 7c, mark changed versions): if you make any changes, you must include a CHANGELOG with all changes and their dates
import fcntl
import glob
import os
import re
import shutil
import socket
import struct
import subprocess

VIDIOC_ENUM_FMT = 0xC0405602
MJPG = int.from_bytes(b"MJPG", "little")


def usb_cameras():
    # by-id names stay the same across reboots and replugs; index0 is the capture node
    return sorted(glob.glob("/dev/v4l/by-id/*-video-index0"))


def libcamera_count():
    tool = shutil.which("rpicam-hello") or shutil.which("libcamera-hello")
    if not tool:
        return 0
    try:
        out = subprocess.run([tool, "--list-cameras"], capture_output=True, text=True, timeout=15).stdout
    except (OSError, subprocess.TimeoutExpired):
        return 0
    return len(re.findall(r"^\s*\d+\s*:", out, re.M))


def has_mjpeg(device):
    try:
        fd = os.open(device, os.O_RDWR | os.O_NONBLOCK)
    except OSError:
        return False
    try:
        for i in range(64):
            # struct v4l2_fmtdesc: index, type (1 = video capture), flags, description[32], pixelformat at byte 44
            buf = bytearray(struct.pack("<III32sII12x", i, 1, 0, b"", 0, 0))
            try:
                fcntl.ioctl(fd, VIDIOC_ENUM_FMT, buf)
            except OSError:
                return False
            if struct.unpack_from("<I", buf, 44)[0] == MJPG:
                return True
        return False
    finally:
        os.close(fd)


def local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("10.255.255.255", 1))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def describe():
    lines = [f"USB: {d} -> {os.path.realpath(d)}{'  (MJPEG)' if has_mjpeg(d) else ''}" for d in usb_cameras()]
    n = libcamera_count()
    if n:
        lines.append(f"Pi camera (libcamera): {n}")
    return lines or ["no cameras found"]
