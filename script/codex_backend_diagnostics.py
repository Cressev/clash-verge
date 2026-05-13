#!/usr/bin/env python3
"""Standalone network diagnostics for Codex backend access."""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import secrets
import socket
import ssl
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

HOST = "chatgpt.com"
PORT = 443
MODELS_PATH = "/backend-api/codex/models?client_version=0.123.0"
COMPACT_PATH = "/backend-api/codex/responses/compact"
WS_PATH = "/backend-api/codex/responses"


@dataclass
class StepResult:
    name: str
    ok: bool
    latency_ms: float | None = None
    status: int | None = None
    reason: str | None = None
    detail: str | None = None
    remote_ip: str | None = None


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def auth_token() -> str | None:
    auth = Path.home() / ".codex" / "auth.json"
    if not auth.exists():
        return None
    try:
        payload = json.loads(auth.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload.get("tokens", {}).get("access_token")


def make_ssl_context() -> ssl.SSLContext:
    return ssl.create_default_context()


def summarize(text: str, limit: int = 200) -> str:
    return " ".join(text.split())[:limit]


def detect_challenge(text: str) -> bool:
    lowered = text.lower()
    markers = (
        "enable javascript and cookies to continue",
        "challenge-error-text",
        "/cdn-cgi/challenge-platform/",
        "__cf_chl_",
    )
    return any(marker in lowered for marker in markers)


def step_dns() -> StepResult:
    start = time.perf_counter()
    try:
        ips = sorted({info[4][0] for info in socket.getaddrinfo(HOST, PORT, type=socket.SOCK_STREAM)})
        return StepResult("dns", True, round((time.perf_counter() - start) * 1000.0, 1), detail=", ".join(ips[:6]), remote_ip=ips[0] if ips else None)
    except Exception as exc:  # noqa: BLE001
        return StepResult("dns", False, round((time.perf_counter() - start) * 1000.0, 1), reason=type(exc).__name__, detail=str(exc))


def step_tcp(timeout: float) -> StepResult:
    start = time.perf_counter()
    try:
        with socket.create_connection((HOST, PORT), timeout=timeout) as sock:
            return StepResult("tcp", True, round((time.perf_counter() - start) * 1000.0, 1), remote_ip=sock.getpeername()[0])
    except Exception as exc:  # noqa: BLE001
        return StepResult("tcp", False, round((time.perf_counter() - start) * 1000.0, 1), reason=type(exc).__name__, detail=str(exc))


def step_tls(timeout: float) -> StepResult:
    ctx = make_ssl_context()
    start = time.perf_counter()
    try:
        with socket.create_connection((HOST, PORT), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=HOST) as tls:
                cert = tls.getpeercert() or {}
                subject = dict(x[0] for x in cert.get("subject", [])) if cert else {}
                return StepResult("tls", True, round((time.perf_counter() - start) * 1000.0, 1), remote_ip=tls.getpeername()[0], detail=f"tls={tls.version()} cn={subject.get('commonName', '?')}")
    except Exception as exc:  # noqa: BLE001
        return StepResult("tls", False, round((time.perf_counter() - start) * 1000.0, 1), reason=type(exc).__name__, detail=str(exc))


def headers(token: str | None) -> dict[str, str]:
    out = {
        "Host": HOST,
        "User-Agent": "clash-verge/codex-backend-diagnostics",
        "Accept": "application/json, text/plain, */*",
    }
    if token:
        out["Authorization"] = f"Bearer {token}"
    return out


def https_get(path: str, timeout: float, token: str | None) -> StepResult:
    ctx = make_ssl_context()
    start = time.perf_counter()
    conn = http.client.HTTPSConnection(HOST, PORT, timeout=timeout, context=ctx)
    try:
        conn.request("GET", path, headers=headers(token))
        resp = conn.getresponse()
        body = resp.read(4096).decode("utf-8", errors="replace")
        remote = conn.sock.getpeername()[0] if conn.sock else None
        challenge = detect_challenge(body)
        ok = (200 <= resp.status < 500) and not challenge
        return StepResult(f"https {path}", ok, round((time.perf_counter() - start) * 1000.0, 1), status=resp.status, reason="cloudflare_challenge" if challenge else resp.reason, detail=summarize(body), remote_ip=remote)
    except Exception as exc:  # noqa: BLE001
        return StepResult(f"https {path}", False, round((time.perf_counter() - start) * 1000.0, 1), reason=type(exc).__name__, detail=str(exc))
    finally:
        conn.close()


def compact_post(timeout: float, token: str | None) -> StepResult:
    ctx = make_ssl_context()
    start = time.perf_counter()
    conn = http.client.HTTPSConnection(HOST, PORT, timeout=timeout, context=ctx)
    try:
        hdr = headers(token)
        hdr["Content-Type"] = "application/json"
        conn.request("POST", COMPACT_PATH, body=b"{}", headers=hdr)
        resp = conn.getresponse()
        body = resp.read(4096).decode("utf-8", errors="replace")
        remote = conn.sock.getpeername()[0] if conn.sock else None
        challenge = detect_challenge(body)
        ok = resp.status in {200, 400, 401, 403, 405, 422} and not challenge
        return StepResult(f"https {COMPACT_PATH}", ok, round((time.perf_counter() - start) * 1000.0, 1), status=resp.status, reason="cloudflare_challenge" if challenge else resp.reason, detail=summarize(body), remote_ip=remote)
    except Exception as exc:  # noqa: BLE001
        return StepResult(f"https {COMPACT_PATH}", False, round((time.perf_counter() - start) * 1000.0, 1), reason=type(exc).__name__, detail=str(exc))
    finally:
        conn.close()


def websocket_probe(timeout: float, token: str | None) -> StepResult:
    ctx = make_ssl_context()
    key = base64.b64encode(secrets.token_bytes(16)).decode("ascii")
    request = "\r\n".join(
        [
            f"GET {WS_PATH} HTTP/1.1",
            f"Host: {HOST}",
            "Upgrade: websocket",
            "Connection: Upgrade",
            "Sec-WebSocket-Version: 13",
            f"Sec-WebSocket-Key: {key}",
            "User-Agent: clash-verge/codex-backend-diagnostics",
            "Origin: https://chatgpt.com",
            f"Authorization: Bearer {token}" if token else "",
            "",
            "",
        ]
    ).encode("ascii")
    start = time.perf_counter()
    try:
        with socket.create_connection((HOST, PORT), timeout=timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=HOST) as tls:
                tls.sendall(request)
                resp = tls.recv(1024).decode("utf-8", errors="replace")
                remote = tls.getpeername()[0]
                ok = "101" in resp.splitlines()[0] if resp else False
                return StepResult("ws", ok, round((time.perf_counter() - start) * 1000.0, 1), detail=summarize(resp), remote_ip=remote)
    except Exception as exc:  # noqa: BLE001
        return StepResult("ws", False, round((time.perf_counter() - start) * 1000.0, 1), reason=type(exc).__name__, detail=str(exc))


def run_once(timeout: float, with_auth: bool) -> list[StepResult]:
    token = auth_token() if with_auth else None
    return [
        step_dns(),
        step_tcp(timeout),
        step_tls(timeout),
        https_get(MODELS_PATH, timeout, token),
        compact_post(timeout, token),
        websocket_probe(timeout, token),
    ]


def print_results(results: list[StepResult]) -> int:
    overall = 0
    for item in results:
        status = "ok" if item.ok else "fail"
        print(f"{item.name:<24} {status:<4} {item.status or ''} {item.reason or ''} {item.detail or ''}".rstrip())
        if not item.ok:
            overall = 1
    return overall


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--auth-mode", choices=["on", "off"], default="on")
    parser.add_argument("--output-json")
    args = parser.parse_args()

    payload: list[dict[str, Any]] = []
    exit_code = 0
    for _ in range(max(1, args.attempts)):
        results = run_once(args.timeout, args.auth_mode == "on")
        exit_code = max(exit_code, print_results(results))
        payload.append({"timestamp": now_iso(), "results": [asdict(item) for item in results]})

    if args.output_json:
        Path(args.output_json).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
