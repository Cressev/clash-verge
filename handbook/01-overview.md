# 01. Overview

这套手册解决的是同一个问题的不同面：

- Clash Verge 开启 TUN 后，外网和内网链路互相抢路由。
- Feilian VPN 需要接管公司域名、DNS 和内网网段。
- Codex 需要稳定访问 `chatgpt.com` 的 HTTPS 和 WebSocket。

## 核心结论

不要只问“代理开没开”。要同时看三层：

1. DNS 是否被 fake-ip 污染。
2. 规则是否真的把目标流量导向正确出口。
3. TUN 路由是否把流量提前截走。

## 参考来源

- session: `019dc51d-e92a-7910-9762-633b0264debc`
- `tools/codex-tun-feilian-fix`
- `tools/codex-backend-diagnostics`

## 适用范围

这本手册偏向“本机网络路径修复与复查”，不是单纯的账号故障排查。
