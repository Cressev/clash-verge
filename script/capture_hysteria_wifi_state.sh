#!/usr/bin/env bash
set -euo pipefail

timestamp="$(date '+%Y%m%d-%H%M%S')"
out_dir="${1:-}"

if [ -z "$out_dir" ]; then
  out_dir="$(mktemp -d "/tmp/clash-verge-hysteria-${timestamp}.XXXXXX")"
fi

mkdir -p "$out_dir"

capture_cmd() {
  local title="$1"
  local file="$2"
  shift 2

  {
    printf '## %s\n\n' "$title"
    printf '$ '
    printf '%q ' "$@"
    printf '\n\n'
    set +e
    "$@"
    local rc=$?
    set -e
    printf '\n[exit:%s]\n' "$rc"
  } >"$file" 2>&1
}

capture_text() {
  local title="$1"
  local file="$2"
  local body="$3"

  {
    printf '## %s\n\n' "$title"
    printf '%s\n' "$body"
  } >"$file"
}

service_dir="$HOME/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev"
service_log="$service_dir/logs/service/service_latest.log"
profiles_yaml="$service_dir/profiles.yaml"
dns_yaml="$service_dir/dns_config.yaml"

capture_text "Run metadata" "$out_dir/00-meta.txt" "$(cat <<EOF
timestamp: $timestamp
out_dir: $out_dir
user: $(whoami)
host: $(hostname)
pwd: $PWD
EOF
)"

capture_cmd "System" "$out_dir/01-system.txt" uname -a
capture_cmd "macOS version" "$out_dir/02-sw_vers.txt" sw_vers
capture_cmd "Network services" "$out_dir/03-network-services.txt" networksetup -listallnetworkservices
capture_cmd "Hardware ports" "$out_dir/04-hardware-ports.txt" networksetup -listallhardwareports
capture_cmd "Default route" "$out_dir/05-default-route.txt" route -n get default

if command -v ifconfig >/dev/null 2>&1; then
  capture_cmd "Interface table" "$out_dir/06-ifconfig.txt" ifconfig
fi

capture_cmd "DNS cache entries" "$out_dir/07-dns-cache.txt" scutil --dns
capture_cmd "System DNS chatgpt.com" "$out_dir/08-chatgpt-dns.txt" dscacheutil -q host -a name chatgpt.com
capture_cmd "System DNS jumpserver.zphz.cn" "$out_dir/09-jumpserver-dns.txt" dscacheutil -q host -a name jumpserver.zphz.cn
capture_cmd "System DNS feilian.zphz.cn" "$out_dir/10-feilian-dns.txt" dscacheutil -q host -a name feilian.zphz.cn

capture_cmd "Proxy env" "$out_dir/11-proxy-env.txt" env
capture_cmd "Relevant processes" "$out_dir/12-processes.txt" pgrep -lf 'clash|verge|mihomo|hysteria|feilian|corplink|ssh|quic|udp' 

if [ -f "$profiles_yaml" ]; then
  capture_cmd "Profiles" "$out_dir/13-profiles.yaml.txt" sed -n '1,260p' "$profiles_yaml"
fi

if [ -f "$dns_yaml" ]; then
  capture_cmd "DNS config" "$out_dir/14-dns-config.yaml.txt" sed -n '1,220p' "$dns_yaml"
fi

if [ -f "$service_log" ]; then
  capture_cmd "Service log tail" "$out_dir/15-service-log-tail.txt" tail -n 300 "$service_log"
  capture_cmd "Service log clues" "$out_dir/16-service-log-clues.txt" rg -n -i 'hysteria|quic|udp|timeout|handshake|reset|refused|closed|error|dns' "$service_log"
fi

manifest="$out_dir/99-manifest.txt"
{
  printf 'capture completed: %s\n' "$timestamp"
  printf 'output directory: %s\n\n' "$out_dir"
  find "$out_dir" -maxdepth 1 -type f | sort
} >"$manifest"

printf '%s\n' "$out_dir"
