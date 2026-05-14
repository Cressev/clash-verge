# script

这里放和 handbook 配套的检查脚本、wrapper 和诊断代码。

## 当前文件

- `check_macos_codex_tun_feilian.sh`: macOS 下检查 Codex / Clash / Feilian / 代理端口。
- `check_windows_feilian_tun.ps1`: Windows 下检查 Clash Verge / Feilian / 路由 / DNS。
- `codex_wrapper.zsh`: Codex wrapper 模板。
- `codex_backend_diagnostics.py`: Codex backend 的网络诊断脚本。
- `capture_hysteria_wifi_state.sh`: zphz WiFi + Hysteria 场景的切前/切后本地快照采集脚本。
- `codex_relay_compact_node_probe.py`: 逐个切换 Clash selector 节点并重复测试 Codex relay compact 接口。

## 使用原则

- 脚本要能说明“测的是哪一层”。
- 诊断脚本尽量保留标准库或最小依赖。
- 如果脚本依赖本机路径，要在 README 里注明。

## Hysteria 快照脚本

典型用法：

```bash
./script/capture_hysteria_wifi_state.sh
```

脚本会把快照写到一个临时目录并打印路径。建议在两次时刻各跑一次：

1. 切换到 Hysteria 节点之前
2. 节点切过去后，如果网络断了，回来再跑一次

重点比较：

- `05-default-route.txt`
- `07-dns-cache.txt`
- `08-chatgpt-dns.txt`
- `09-jumpserver-dns.txt`
- `13-profiles.yaml.txt`
- `14-dns-config.yaml.txt`
- `15-service-log-tail.txt`
- `16-service-log-clues.txt`

## Codex relay compact 节点探针

典型用法：

```bash
./script/codex_relay_compact_node_probe.py --attempts 3
```

默认行为：

- 读取 `~/.codex/config.toml` 的当前 provider `base_url`
- 读取 `~/.codex/auth.json` 或 `OPENAI_API_KEY`
- 通过 `/tmp/verge/verge-mihomo.sock` 控制 `节点选择`
- 通过 `http://127.0.0.1:7897` 请求 relay API
- 每个节点测试 `/v1/responses/compact` 和 `/v1/models`
- 结束后恢复原始 selector 节点

输出 JSON 默认写到 `/tmp/codex-compact-node-results-*.json`。脚本不会打印 API key。
