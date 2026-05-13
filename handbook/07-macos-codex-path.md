# 07. macOS + Codex Path

## 结论

macOS 上 Codex 能不能稳定，不只取决于 `codex` 命令本身，还取决于它有没有走和诊断工具一致的代理路径。

## wrapper

```zsh
REAL_CODEX="/Users/liam/.nvm/versions/node/v22.22.2/bin/codex"
CLASH_PROXY="http://127.0.0.1:7897"
```

如果本地代理端口可用，wrapper 就给 `codex` 注入代理环境。

## 检查方式

```bash
which codex
sed -n '1,80p' ~/.local/bin/codex
nc -z 127.0.0.1 7897 && echo proxy-ok
```

## 诊断思路

- `codex-switch doctor` 和 `bal` 也要走同一套代理路径。
- 新开 shell 时，不能默认它已经继承了你想要的代理变量。
- 如果 `chatgpt.com` 的 TLS 证书出现 hostname mismatch，先怀疑路径，不要先怀疑账号。
