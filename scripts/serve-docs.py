# /// script
# requires-python = ">=3.10"
# dependencies = ["watchfiles"]
# ///
"""Serve docs/ with live reload. Files are watched for changes and the browser auto-refreshes."""

from __future__ import annotations

import http.server
import io
import queue
import threading
import webbrowser
from pathlib import Path
from typing import IO

from watchfiles import watch

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
PORT = 8000
RELOAD_CLIENTS: list[queue.Queue[str]] = []

# JavaScript injected into every HTML response for live reload
RELOAD_SCRIPT = b"""
<script>
(function() {
  function connect() {
    var es = new EventSource('/__reload');
    es.onmessage = function() { location.reload(); };
    es.onerror = function() { es.close(); setTimeout(connect, 1000); };
  }
  connect();
})();
</script>
"""


class ReloadHandler(http.server.SimpleHTTPRequestHandler):
    """Serves files from docs/ and injects live-reload script into HTML."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/__reload":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            q: queue.Queue[str] = queue.Queue()
            RELOAD_CLIENTS.append(q)
            try:
                while True:
                    msg = q.get()
                    self.wfile.write(f"data: {msg}\n\n".encode())
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, OSError):
                pass
            finally:
                RELOAD_CLIENTS.remove(q)
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):  # type: ignore[override]
        result = super().send_head()
        if result is None:
            return None
        is_html = self.path.endswith((".html", "/")) or self.path == "/"
        if is_html:
            content = result.read()
            result.close()
            if b"</body>" in content:
                content = content.replace(b"</body>", RELOAD_SCRIPT + b"</body>")
            return io.BytesIO(content)
        return result

    def log_message(self, format, *args):
        if "/__reload" not in str(args[0]):
            super().log_message(format, *args)


def notify_clients():
    for q in RELOAD_CLIENTS:
        try:
            q.put_nowait("reload")
        except queue.Full:
            pass


def watch_files():
    for _ in watch(DOCS_DIR):
        notify_clients()


def main():
    watcher = threading.Thread(target=watch_files, daemon=True)
    watcher.start()

    port = PORT
    for attempt in range(10):
        try:
            server = http.server.HTTPServer(("", port), ReloadHandler)
            break
        except OSError:
            port += 1
    else:
        print(f"Could not find an open port in range {PORT}-{port}")
        return

    url = f"http://localhost:{port}"
    print(f"  Docs:   {url}")
    print(f"  Watch:  {DOCS_DIR}")
    print(f"  Press Ctrl+C to stop\n")

    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
