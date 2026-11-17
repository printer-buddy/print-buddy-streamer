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
import argparse
import logging
import os
import sys

from . import config, detect, manager


def main():
    ap = argparse.ArgumentParser(prog="streamer", description="Print Buddy Streamer")
    ap.add_argument("-c", "--config", default="streamer.conf")
    ap.add_argument("--list", action="store_true", help="show the cameras found and exit")
    a = ap.parse_args()
    if a.list:
        print("\n".join(detect.describe()))
        return 0
    cfg = config.load(a.config)
    logging.basicConfig(level=getattr(logging, cfg.log_level.upper(), logging.INFO),
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return manager.Supervisor(cfg, os.path.dirname(os.path.abspath(a.config))).run()


if __name__ == "__main__":
    sys.exit(main())
