#!/usr/bin/env python3
"""Simple log checking utility.

Usage: python check_logs.py [--file FILE] [--lines N] [--filter KEYWORD] [--level LEVEL] [--follow]

Defaults to `/var/log/syslog` or `/var/log/messages` depending on availability.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Optional


def default_log_file() -> str:
    candidates = ['/var/log/syslog', '/var/log/messages']
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


def tail_file(path: str, n: int = 200, follow: bool = False):
    try:
        with open(path, 'r', errors='replace') as f:
            # Seek to last n lines
            if n > 0:
                try:
                    f.seek(0, os.SEEK_END)
                    filesize = f.tell()
                    blocksize = 1024
                    data = ''
                    while len(data.splitlines()) <= n and filesize > 0:
                        readsize = min(blocksize, filesize)
                        f.seek(filesize - readsize)
                        chunk = f.read(readsize)
                        data = chunk + data
                        filesize -= readsize
                    lines = data.splitlines()
                    to_show = lines[-n:]
                except Exception:
                    f.seek(0)
                    to_show = f.readlines()[-n:]
            else:
                to_show = f.readlines()

            for L in to_show:
                yield L.rstrip('\n')

            if follow:
                while True:
                    where = f.tell()
                    line = f.readline()
                    if not line:
                        time.sleep(0.5)
                        f.seek(where)
                    else:
                        yield line.rstrip('\n')
    except PermissionError:
        raise
    except FileNotFoundError:
        raise


def matches(line: str, keyword: Optional[str], level: Optional[str]) -> bool:
    if keyword and keyword.lower() not in line.lower():
        return False
    if level:
        lvl = level.lower()
        if lvl == 'error' and 'error' not in line.lower() and 'err' not in line.lower():
            return False
        if lvl == 'warn' and ('warn' not in line.lower() and 'warning' not in line.lower()):
            return False
        if lvl == 'info' and 'info' not in line.lower():
            return False
    return True


def main():
    parser = argparse.ArgumentParser(description='Check system logs (simple viewer/filter)')
    parser.add_argument('--file', '-f', help='Path to log file', default=None)
    parser.add_argument('--lines', '-n', type=int, default=200, help='How many lines to show')
    parser.add_argument('--filter', '-k', dest='keyword', help='Keyword to filter (case-insensitive)')
    parser.add_argument('--level', '-l', choices=['error', 'warn', 'info'], help='Filter by level')
    parser.add_argument('--follow', action='store_true', help='Follow (tail -f)')
    args = parser.parse_args()

    path = args.file or default_log_file()

    try:
        for line in tail_file(path, n=args.lines, follow=args.follow):
            try:
                if matches(line, args.keyword, args.level):
                    print(line)
            except Exception:
                # Protect matching from weird encodings
                print(line)
    except PermissionError:
        print(f'Permission denied reading {path} — try running with sudo', file=sys.stderr)
        sys.exit(2)
    except FileNotFoundError:
        print(f'Log file {path} not found', file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
