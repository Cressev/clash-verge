# script

这里放和 handbook 配套的检查脚本、wrapper 和诊断代码。

## 当前文件

- `check_macos_codex_tun_feilian.sh`: macOS 下检查 Codex / Clash / Feilian / 代理端口。
- `check_windows_feilian_tun.ps1`: Windows 下检查 Clash Verge / Feilian / 路由 / DNS。
- `codex_wrapper.zsh`: Codex wrapper 模板。
- `codex_backend_diagnostics.py`: Codex backend 的网络诊断脚本。

## 使用原则

- 脚本要能说明“测的是哪一层”。
- 诊断脚本尽量保留标准库或最小依赖。
- 如果脚本依赖本机路径，要在 README 里注明。
