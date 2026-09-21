#!/usr/bin/env python3
"""One-shot Laya predict. Uses the resident server when it is up."""
import argparse
import json
import sys
import urllib.error
import urllib.request

from runtime import HOST, PORT, load_agent, questions_for


def _server_up():
    try:
        with urllib.request.urlopen(f"http://{HOST}:{PORT}/health", timeout=0.4) as resp:
            return resp.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def _post(payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"http://{HOST}:{PORT}/predict",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def _read_state(args):
    if args.file:
        with open(args.file) as f:
            raw = f.read()
    elif args.text:
        raw = " ".join(args.text)
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    else:
        raise SystemExit("usage: laya-ask [--preset triage] \"user text\"")
    raw = raw.strip()
    if not raw:
        raise SystemExit("empty input")
    if raw[0] in "{[":
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    return raw


def main():
    parser = argparse.ArgumentParser(description="Run one Laya decision")
    parser.add_argument("text", nargs="*", help="user text")
    parser.add_argument("--preset", default="default")
    parser.add_argument("--file", help="text or JSON state file")
    parser.add_argument("--local", action="store_true", help="ignore the resident server")
    args = parser.parse_args()
    state = _read_state(args)
    questions = questions_for(args.preset)
    payload = {"state": state, "preset": args.preset}
    if not args.local and _server_up():
        result = _post(payload)
        result["via"] = "server"
    else:
        agent = load_agent()
        result = agent.predict(state, questions)
        from mape.monitor import record
        result["events"] = record(state, questions, result)
        result["via"] = "local"
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
