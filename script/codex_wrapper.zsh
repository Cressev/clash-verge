#!/bin/zsh

# Wrapper used on macOS when Feilian VPN and Clash/Mihomo TUN are both enabled.
# Update REAL_CODEX to match the local Codex installation path if needed.

REAL_CODEX="/Users/liam/.nvm/versions/node/v22.22.2/bin/codex"
CLASH_PROXY="http://127.0.0.1:7897"

if /usr/bin/nc -z 127.0.0.1 7897 >/dev/null 2>&1; then
  export HTTP_PROXY="$CLASH_PROXY"
  export HTTPS_PROXY="$CLASH_PROXY"
  export ALL_PROXY="$CLASH_PROXY"
  export http_proxy="$CLASH_PROXY"
  export https_proxy="$CLASH_PROXY"
  export all_proxy="$CLASH_PROXY"
  export NO_PROXY="localhost,127.0.0.1,::1,*.local,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"
  export no_proxy="$NO_PROXY"
fi

exec "$REAL_CODEX" "$@"
