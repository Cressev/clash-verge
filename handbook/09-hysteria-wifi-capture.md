# 09. Hysteria WiFi Capture

## 目的

这类问题不能靠“边切节点边聊天”解决，所以先采集、后分析。

## 采集时机

1. 切换到 Hysteria 节点前。
2. 节点切过去后，如果网络断了，再采一次。

## 看什么

- 默认路由有没有变。
- 系统 DNS 和 Clash DNS 有没有出现异常。
- `profiles.yaml` / `dns_config.yaml` 里当前 profile 和规则有没有变化。
- Clash Verge service log 里有没有 `hysteria`、`quic`、`udp`、`timeout`、`handshake` 之类的线索。

## 快速命令

```bash
./script/capture_hysteria_wifi_state.sh
```

脚本会返回一个临时目录路径，里面就是快照材料。

## 复盘方式

把“切前”和“切后”的两个目录放一起比较。先看路由和 DNS，再看配置文件，最后看日志。
