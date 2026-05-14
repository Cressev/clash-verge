# Official compact node stability on zphz WiFi, excluding HY2

Date: 2026-05-14

Scope:
- Network: zphz WiFi
- Target: `https://chatgpt.com/backend-api/codex/responses/compact`
- Selector under test: `节点选择`
- Proxy under test: Clash Verge local proxy `http://127.0.0.1:7897`
- Attempts: 5 per non-HY2 selector entry
- Skipped HY2 nodes: `日本JP-HY2`, `新加坡SG-HY2`, `香港HK-HY2`, `韩国KR-HY2`, `德国DE-HY2`
- Raw result: `/tmp/official-compact-non-hy2-node-results-20260514-110945.json`

Interpretation:
- The current Codex client is not authenticated against official ChatGPT, so HTTP `401` is expected and is treated as a successful network/application-layer reachability signal.
- Timeout, SSL EOF, and SSL handshake timeout are treated as unstable.
- The test restored the original selector value: `新加坡-优化-Gemini-GPT`.
- Subscription metadata selector entries such as `剩余流量：...` and `套餐到期：...` are ignored in the recommendations.

## Best smooth candidates

These real nodes reached official compact `5/5` and had no run at or above 4 seconds.

| Node | Compact | Avg | Max |
| --- | ---: | ---: | ---: |
| 德国-优化 | 5/5 | 1.832s | 1.944s |
| 加拿大-优化2 | 5/5 | 1.832s | 2.073s |
| 印度-优化 | 5/5 | 1.857s | 1.968s |
| 尼日利亚NG-A | 5/5 | 1.863s | 2.082s |
| 新加坡-优化-Gemini-GPT | 5/5 | 1.881s | 2.002s |
| 台湾-优化2-GPT | 5/5 | 1.894s | 2.114s |
| 美国LA-优化3-GPT | 5/5 | 1.898s | 2.134s |
| 日本-优化 | 5/5 | 1.939s | 2.034s |
| 日本-优化3 | 5/5 | 1.942s | 2.037s |
| 新加坡SG-A-Gemini | 5/5 | 1.942s | 2.038s |
| 加拿大-优化 | 5/5 | 1.946s | 2.050s |
| 越南VN-A | 5/5 | 1.968s | 2.059s |
| 日本-优化2 | 5/5 | 1.970s | 2.041s |
| 香港-优化-Gemini | 5/5 | 1.970s | 2.076s |
| 美国LA-优化2-GPT | 5/5 | 1.971s | 2.098s |
| 英国-优化-GPT | 5/5 | 1.985s | 2.033s |
| 乌克兰UA-A | 5/5 | 2.005s | 2.318s |
| 新加坡-优化2-Gemini-GPT | 5/5 | 2.005s | 2.381s |
| 德国-优化2 | 5/5 | 2.058s | 2.467s |

Practical first choices:

1. `新加坡-优化-Gemini-GPT`
2. `日本-优化`
3. `日本-优化2`
4. `日本-优化3`
5. `香港-优化-Gemini`
6. `印度-优化`
7. `德国-优化`

The table is sorted by measured average latency, but the practical list favors nodes that are likely to be reasonable long-session choices from this region.

## Reachable but spiky

These nodes reached official compact `5/5`, but had one or more slow spikes or a higher max latency. They are acceptable fallbacks, not first choices for compact-heavy Codex sessions.

| Node | Compact | Avg | Max | Slow runs >=4s |
| --- | ---: | ---: | ---: | ---: |
| 香港HKT-A | 5/5 | 2.002s | 2.507s | 0 |
| 香港HK-A-Gemini | 5/5 | 2.053s | 2.664s | 0 |
| 日本JP-A | 5/5 | 2.117s | 2.824s | 0 |
| 香港WAP-优化-Gemini | 5/5 | 2.125s | 2.779s | 0 |
| 英国-优化2 | 5/5 | 2.127s | 2.593s | 0 |
| 土耳其TR-A | 5/5 | 2.143s | 2.637s | 0 |
| 台湾-优化3 | 5/5 | 2.471s | 4.944s | 1 |
| 美国LA-优化-GPT | 5/5 | 2.600s | 5.376s | 1 |
| 香港WAP-优化3-Gemini | 5/5 | 2.640s | 5.865s | 1 |
| 新加坡-优化3-Gemini | 5/5 | 2.658s | 5.800s | 1 |
| 香港-优化2-Gemini | 5/5 | 2.673s | 6.544s | 1 |
| 加拿大-优化3 | 5/5 | 2.837s | 6.726s | 1 |
| 香港-优化3-Gemini | 5/5 | 2.868s | 6.498s | 1 |
| 俄罗斯RU-A | 5/5 | 2.961s | 6.820s | 1 |
| 台湾-优化 | 5/5 | 3.110s | 5.550s | 2 |
| 香港WAP-优化2-Gemini | 5/5 | 3.466s | 6.759s | 2 |
| 英国-优化3 | 5/5 | 3.794s | 6.855s | 2 |

## Avoid

| Node | Compact | Failure |
| --- | ---: | --- |
| 美国USLA-A | 4/5 | one SSL handshake timeout |

## Conclusion

Under zphz WiFi, once the currently-broken HY2 nodes are excluded, most TCP/TLS-style nodes can still reach the official ChatGPT Codex compact endpoint. The best alternatives to the previously stable Hysteria path are the smooth `5/5` nodes above, especially `新加坡-优化-Gemini-GPT`, the `日本-优化*` group, `香港-优化-Gemini`, `印度-优化`, and `德国-优化`.
