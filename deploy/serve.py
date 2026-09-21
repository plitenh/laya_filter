#!/usr/bin/env python3
"""Resident Laya server. The INT8 model stays loaded until the process exits."""
import json
import os
import signal
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from runtime import HOST, PORT, load_agent, questions_for

PID_PATH = os.path.join(os.path.dirname(__file__), "laya-serve.pid")
LOG_PATH = os.path.join(os.path.dirname(__file__), "laya-serve.log")

AGENT = None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.rstrip("/") == "/health":
            self._send(200, {"ok": True, "model": "laya-large-int8"})
            return
        self._send(404, {"error": "not found"})

    def do_POST(self):
        path = self.path.rstrip("/")
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except Exception as exc:
            self._send(400, {"error": str(exc)})
            return
        if path == "/predict":
            try:
                state = payload.get("state")
                if state is None:
                    raise ValueError("missing state")
                if "questions" in payload:
                    questions = payload["questions"]
                else:
                    questions = questions_for(payload.get("preset", "default"))
                result = AGENT.predict(state, questions)
                self._send(200, result)
            except Exception as exc:
                self._send(400, {"error": str(exc)})
            return
        self._send(404, {"error": "not found"})


def _running_pid():
    if not os.path.exists(PID_PATH):
        return None
    try:
        pid = int(open(PID_PATH).read().strip())
    except ValueError:
        return None
    try:
        os.kill(pid, 0)
    except OSError:
        return None
    return pid


def _healthy():
    try:
        with urllib.request.urlopen(f"http://{HOST}:{PORT}/health", timeout=0.5) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def serve_foreground():
    global AGENT
    AGENT = load_agent()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"laya-serve listening on http://{HOST}:{PORT}", flush=True)
    httpd.serve_forever()


def serve_background():
    pid = _running_pid()
    if pid and _healthy():
        print(f"already running pid={pid} http://{HOST}:{PORT}")
        return
    if os.fork() > 0:
        for _ in range(120):
            if _healthy():
                print(f"laya-serve up http://{HOST}:{PORT}")
                return
            time.sleep(0.5)
        print("laya-serve failed to become healthy; see", LOG_PATH, file=sys.stderr)
        sys.exit(1)
    os.setsid()
    log = open(LOG_PATH, "a", buffering=1)
    os.dup2(log.fileno(), 1)
    os.dup2(log.fileno(), 2)
    with open(PID_PATH, "w") as f:
        f.write(str(os.getpid()))
    try:
        serve_foreground()
    finally:
        if os.path.exists(PID_PATH):
            os.remove(PID_PATH)


def stop():
    pid = _running_pid()
    if not pid:
        print("laya-serve is not running")
        return
    os.kill(pid, signal.SIGTERM)
    for _ in range(40):
        if _running_pid() is None:
            break
        time.sleep(0.1)
    if os.path.exists(PID_PATH):
        os.remove(PID_PATH)
    print(f"stopped pid={pid}")


def main():
    if "--stop" in sys.argv:
        stop()
    elif "--bg" in sys.argv:
        serve_background()
    else:
        serve_foreground()


if __name__ == "__main__":
    main()
