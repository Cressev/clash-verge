# zphz WiFi + Hysteria

在 zphz WiFi 下，Hysteria 节点出现稳定超时，而同一张 WiFi 上切回 vmess 节点后又恢复。

## 采集结论

- 三次快照里，默认路由相同，DNS 配置相同，Clash Verge profile 结构相同。
- 变化只在当前选中的节点。
- Hysteria 那次服务日志里反复出现 `planb.mojcn.com:16618` 的 `operation was canceled` 和 `context deadline exceeded`。
- 切回 vmess 后，`google.com`、`github.com`、`chatgpt.com` 重新恢复。

## 解释

这更像是 zphz WiFi 对 Hysteria / UDP / QUIC 路径不稳定，而不是本机 Clash Verge 的全局配置问题。

## 处理顺序

1. 如果节点或服务端支持，先尝试降低 Hysteria 的 MTU / packet size。
2. 同时避免让 DNS 依赖不稳定的 UDP 路径。
3. 如果仍然超时，基本可以判断这张 WiFi 对 Hysteria 不兼容，只能换回 TCP 类协议或换出口。
