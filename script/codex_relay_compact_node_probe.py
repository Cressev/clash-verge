#!/usr/bin/env python3
"""Probe Codex relay compact reachability across Clash selector nodes.

The compact endpoint is intentionally called with an empty JSON object. For the
current relay API, HTTP 400 with "model is required" means the request reached
the authenticated application path; transport errors, timeouts, and 403 are not
treated as compact success.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import http.client
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None


DEFAULT_SOCKET = "/tmp/verge/verge-mihomo.sock"
DEFAULT_SECRET = "set-your-secret"
DEFAULT_GROUP = "节点选择"
DEFAULT_PROXY = "http://127.0.0.1:7897"
DEFAULT_CONFIG = Path.home() / ".codex" / "config.toml"
DEFAULT_AUTH = Path.home() / ".codex" / "auth.json"


class UnixHTTPConnection(http.client.HTTPConnection):
    unix_socket_path = DEFAULT_SOCKET

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.unix_socket_path)


class UnixHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(UnixHTTPConnection, req)


def load_codex_base_url(config_path: Path) -> str:
    if tomllib is None or not config_path.exists():
        return ""
    data = tomllib.loads(config_path.read_text())
    provider = data.get("model_provider")
    providers = data.get("model_providers", {})
    if provider and provider in providers:
        return str(providers[provider].get("base_url", "")).rstrip("/")
    return ""


def load_api_key(auth_path: Path) -> str:
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key
    if not auth_path.exists():
        return ""
    data = json.loads(auth_path.read_text())
    for key in ("OPENAI_API_KEY", "api_key", "access_token"):
        value = data.get(key)
        if value:
            return str(value)
    return ""


def build_clash_opener(socket_path: str) -> urllib.request.OpenerDirector:
    UnixHTTPConnection.unix_socket_path = socket_path
    return urllib.request.build_opener(UnixHTTPHandler)


def clash_request(opener, method: str, path: str, secret: str, body=None, timeout=5):
    data = None
    headers = {"Authorization": f"Bearer {secret}"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        f"http://unix{path}",
        data=data,
        headers=headers,
        method=method,
    )
    with opener.open(req, timeout=timeout) as resp:
        payload = resp.read()
    return json.loads(payload.decode("utf-8")) if payload else {}


def get_selector(opener, group: str, secret: str, timeout: float):
    encoded = urllib.parse.quote(group, safe="")
    return clash_request(opener, "GET", f"/proxies/{encoded}", secret, timeout=timeout)


def set_selector(opener, group: str, node: str, secret: str, timeout: float) -> None:
    encoded = urllib.parse.quote(group, safe="")
    clash_request(opener, "PUT", f"/proxies/{encoded}", secret, {"name": node}, timeout)


def timed_request(opener, req: urllib.request.Request, timeout: float, ok_statuses: set[int]):
    start = time.monotonic()
    status = None
    err = ""
    body = ""
    ok = False
    try:
        with opener.open(req, timeout=timeout) as resp:
            status = resp.status
            body = resp.read(512).decode("utf-8", "replace")
        ok = status in ok_statuses
    except urllib.error.HTTPError as exc:
        status = exc.code
        err = "HTTPError"
        body = exc.read(512).decode("utf-8", "replace")
        ok = status in ok_statuses
    except Exception as exc:  # noqa: BLE001 - diagnostic script should capture all failures
        err = f"{type(exc).__name__}: {exc}"
    return {
        "ok": ok,
        "status": status,
        "time": round(time.monotonic() - start, 3),
        "err": err,
        "body_sample": body[:160],
    }


def endpoint_request(url: str, api_key: str, method: str, body: bytes | None = None):
    headers = {"Authorization": f"Bearer {api_key}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    return urllib.request.Request(url, data=body, headers=headers, method=method)


def summarize(results):
    rows = []
    for item in results:
        compact = item["compact"]
        ok_count = sum(1 for run in compact if run["ok"])
        avg_time = round(sum(run["time"] for run in compact) / len(compact), 3)
        errors = collections.Counter(run["err"] for run in compact if not run["ok"])
        rows.append(
            {
                "node": item["node"],
                "ok_count": ok_count,
                "avg_time": avg_time,
                "errors": dict(errors),
            }
        )
    return sorted(rows, key=lambda row: (-row["ok_count"], row["avg_time"], row["node"]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--socket", default=DEFAULT_SOCKET)
    parser.add_argument("--secret", default=os.environ.get("CLASH_API_SECRET", DEFAULT_SECRET))
    parser.add_argument("--group", default=DEFAULT_GROUP)
    parser.add_argument("--proxy", default=DEFAULT_PROXY)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--auth", type=Path, default=DEFAULT_AUTH)
    parser.add_argument("--base-url", default="")
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=8)
    parser.add_argument("--settle", type=float, default=1.2)
    parser.add_argument("--compact-ok-status", type=int, nargs="+", default=[400])
    parser.add_argument("--models-ok-status", type=int, nargs="+", default=[200])
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    base_url = (args.base_url or load_codex_base_url(args.config)).rstrip("/")
    api_key = load_api_key(args.auth)
    if not base_url:
        print("error: no relay base_url found; pass --base-url", file=sys.stderr)
        return 2
    if not api_key:
        print("error: no API key found in env or auth file", file=sys.stderr)
        return 2

    clash = build_clash_opener(args.socket)
    proxy_opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": args.proxy, "https": args.proxy})
    )

    selector = get_selector(clash, args.group, args.secret, args.timeout)
    original = selector.get("now")
    nodes = selector.get("all") or []
    if not original or not nodes:
        print(f"error: selector {args.group!r} did not return now/all", file=sys.stderr)
        return 2

    output = args.output
    if not output:
        stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        output = f"/tmp/codex-compact-node-results-{stamp}.json"

    print(f"original: {original}")
    print(f"nodes: {len(nodes)}")

    results = []
    try:
        for index, node in enumerate(nodes, start=1):
            print(f"\n[{index}/{len(nodes)}] {node}", flush=True)
            set_selector(clash, args.group, node, args.secret, args.timeout)
            time.sleep(args.settle)
            item = {"node": node, "compact": [], "models": []}
            for run in range(1, args.attempts + 1):
                compact_req = endpoint_request(
                    f"{base_url}/v1/responses/compact", api_key, "POST", b"{}"
                )
                models_req = endpoint_request(f"{base_url}/v1/models", api_key, "GET")
                compact = timed_request(
                    proxy_opener, compact_req, args.timeout, set(args.compact_ok_status)
                )
                models = timed_request(
                    proxy_opener, models_req, args.timeout, set(args.models_ok_status)
                )
                item["compact"].append(compact)
                item["models"].append(models)
                print(
                    "  run "
                    f"{run}: compact status={compact['status']} ok={compact['ok']} "
                    f"t={compact['time']} err={compact['err']} | "
                    f"models status={models['status']} ok={models['ok']} "
                    f"t={models['time']} err={models['err']}",
                    flush=True,
                )
            results.append(item)
    finally:
        set_selector(clash, args.group, original, args.secret, args.timeout)
        print(f"\nrestored: {original}")

    payload = {
        "base_url": base_url,
        "group": args.group,
        "original": original,
        "attempts": args.attempts,
        "timeout": args.timeout,
        "results": results,
    }
    Path(output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")

    print("\nSUMMARY")
    for row in summarize(results):
        label = "stable" if row["ok_count"] == args.attempts else "partial"
        if row["ok_count"] == 0:
            label = "bad"
        print(
            f"{label:<7} compact={row['ok_count']}/{args.attempts} "
            f"avg={row['avg_time']} node={row['node']} errors={row['errors']}"
        )
    print(f"json: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
