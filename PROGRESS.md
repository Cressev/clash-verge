# PROGRESS

## 阶段 1

- 已把源会话和两套参考工具的内容读完。
- 已确认核心结论：DNS、规则、TUN 路由必须一起看。
- 已在 `clash-verge` 下创建仓库骨架。

## 阶段 2

- 正在把经验拆成 handbook 的独立章节。
- 正在把脚本和代码文件收拢到 `script/`。

## 阶段 3

- GitHub 远程仓库已创建并推送。
- 本地已形成首个可追溯 commit。
- 正在做最终收尾与状态归档。

## 阶段 4

- 正在加入一个“切前/切后”本地采集脚本。
- 目标是让断网的 Hysteria 测试也能事后复盘。
- 已完成三次快照采集，并确认问题更像 Hysteria/UDP 路径不稳定。

## 阶段 5

- 正在判断这类问题能否靠配置修到可用。
- 目前更像协议路径与当前 WiFi 兼容性问题。
- 当前 ChatGPT selector 的网络探针已通，但 Codex compact / websocket 返回 401，说明是认证层而不是路由层。

## 阶段 6

- 正在对同一条路径重复测多轮。
- 目标是确认 401 / timeout 是否稳定，还是偶发抖动。
- 三轮重复探针结果一致，说明当前问题更像认证/应用层而不是纯网络波动。

## 阶段 7

- 已按用户澄清改为测试中转 API `https://www.fhl.mom`，不再把官方 ChatGPT 401 当作目标问题。
- 已逐个切换 `节点选择` 的 42 个节点，每个节点对 `/v1/responses/compact` 重复 3 次。
- 已确认 HY2/Hysteria 类节点在 zphz WiFi 下对 compact 仍是 0/3，近端 TCP/TLS 节点更稳定。

## 阶段 8

- 已按用户纠正切回真正目标：官网 `chatgpt.com/backend-api/codex/responses/compact`。
- 已排除当前 zphz WiFi 下必挂的 5 个 HY2 节点，对剩余 selector 项做 5 轮官网 compact 探针。
- 结论：除 `美国USLA-A` 出现一次 TLS handshake timeout 外，多数非 HY2 节点均能 5/5 到达官网 compact；首选看无 4 秒以上尖峰的节点。

## 阶段 9

- 已按用户亲测反馈重新设计更接近自动 compact 的 64 KiB payload soak。
- 已复现 `新加坡-优化-Gemini-GPT` 频繁失败：15/25，10 次 EOF/timeout。
- 已找到三组更稳候选：`越南VN-A`、`乌克兰UA-A`、`新加坡-优化2-Gemini-GPT`，均为 12/12 且无 4 秒以上长尾。
