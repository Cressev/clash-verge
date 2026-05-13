#!/usr/bin/env bash
set -u

echo "== Codex command =="
if command -v codex >/dev/null 2>&1; then
  CODEX_PATH="$(command -v codex)"
  echo "codex: $CODEX_PATH"
  if [ -f "$CODEX_PATH" ]; then
    echo "-- first lines --"
    sed -n '1,40p' "$CODEX_PATH"
  fi
else
  echo "codex: not found"
fi

echo
echo "== Proxy env =="
env | grep -Ei '^(https?|all|no)_proxy=' || true

echo
echo "== Common local proxy ports =="
for port in 7897 7890 7891 8080; do
  if nc -z 127.0.0.1 "$port" >/dev/null 2>&1; then
    echo "127.0.0.1:$port open"
  else
    echo "127.0.0.1:$port closed"
  fi
done

echo
echo "== Processes =="
pgrep -lf 'clash|verge|mihomo|surge|v2ray|xray|sing-box|tailscale|warp|FeiLian|feilian|Corplink|corplink' || true

echo
echo "== DNS and route =="
dscacheutil -q host -a name chatgpt.com | sed -n '1,20p' || true
CHATGPT_IP="$(dscacheutil -q host -a name chatgpt.com | awk '/ip_address/ {print $2; exit}')"
if [ -n "${CHATGPT_IP:-}" ]; then
  route -n get "$CHATGPT_IP" 2>/dev/null | awk '/interface:|gateway:/ {print}'
fi

echo
echo "== codex-switch doctor =="
if command -v codex-switch >/dev/null 2>&1; then
  codex-switch doctor
else
  echo "codex-switch: not found"
fi

echo
echo "== no-env doctor simulation =="
if command -v codex-switch >/dev/null 2>&1; then
  HTTPS_PROXY= HTTP_PROXY= ALL_PROXY= https_proxy= http_proxy= all_proxy= codex-switch doctor
else
  echo "codex-switch: not found"
fi
