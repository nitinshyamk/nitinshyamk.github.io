#!/usr/bin/env python3
"""Preview the site locally: rebuild on every source edit, serve on :8000.

    python3 serve.py [port]

Serves from the repo root so the root-absolute paths in the page (/style.css,
/images/..., /files/...) resolve exactly as they do on GitHub Pages, redirect
stubs included. Responses carry no-cache headers so a plain refresh is enough
after an edit -- no hard refresh needed.

Sources are polled rather than watched: stdlib has no portable file-watch API,
and a 40-file stat sweep twice a second is free at this size.
"""
import http.server
import subprocess
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INTERVAL = 0.5

# Inputs only. The generated HTML must stay out of this, or writing it would
# look like an edit and the rebuild would trigger itself forever.
SOURCES = ("content/**/*.md", "template.html", "style.css", "build.py")


def snapshot():
    """Modification times of every build input, keyed by path."""
    stamps = {}
    for pattern in SOURCES:
        for path in ROOT.glob(pattern):
            try:
                stamps[path] = path.stat().st_mtime
            except OSError:  # deleted mid-sweep; the next sweep settles it
                pass
    return stamps


def build():
    """Run the real build in a subprocess so a broken build can't kill us."""
    done = subprocess.run(
        [sys.executable, str(ROOT / "build.py")],
        cwd=ROOT, capture_output=True, text=True,
    )
    stamp = time.strftime("%H:%M:%S")
    if done.returncode == 0:
        print(f"[{stamp}] rebuilt")
    else:
        print(f"[{stamp}] BUILD FAILED\n{(done.stderr or done.stdout).strip()}")
    return done.returncode == 0


def watch():
    previous = snapshot()
    while True:
        time.sleep(INTERVAL)
        current = snapshot()
        if current != previous:
            changed = sorted(
                path.relative_to(ROOT).as_posix()
                for path in set(current) ^ set(previous)
                | {p for p in set(current) & set(previous) if current[p] != previous[p]}
            )
            print(f"changed: {', '.join(changed)}")
            build()
            # Re-snapshot after building: the build's own writes are excluded,
            # but an editor may have touched a source again while it ran.
            previous = snapshot()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        if not self.path.startswith(("/images/", "/files/")):
            sys.stderr.write(f"  {fmt % args}\n")


def main():
    # Line-buffer stdout so rebuild status shows up immediately even when
    # this is piped to a log rather than a terminal.
    sys.stdout.reconfigure(line_buffering=True)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    if not build():
        return 1
    threading.Thread(target=watch, daemon=True).start()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"\n  http://localhost:{port}/   (watching {', '.join(SOURCES)}; ctrl-c to stop)\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
