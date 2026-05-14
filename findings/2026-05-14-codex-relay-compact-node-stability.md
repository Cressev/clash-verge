# Codex relay compact node stability on zphz WiFi

Correction note:
- This finding tests the relay API at `www.fhl.mom`, not the official ChatGPT Codex compact endpoint.
- It is useful only for relay-path diagnosis.
- For the user's actual question about official compact reachability while excluding currently-broken HY2 nodes, see `2026-05-14-official-compact-non-hy2-node-stability.md`.

Date: 2026-05-14

Scope:
- Network: zphz WiFi
- Codex API path: `https://www.fhl.mom/v1/responses/compact`
- Proxy under test: Clash Verge local proxy `http://127.0.0.1:7897`
- Selector under test: `节点选择`
- Attempts: 3 per node
- Raw result: `/tmp/codex-compact-node-results-20260514-105525.json`

Interpretation:
- `compact` HTTP `400` is treated as reachable because the relay returned the expected application-layer validation error for an empty request body.
- Transport timeouts, SSL EOF, and `403` are treated as not suitable for Codex compact.
- The test restored the original selector value: `新加坡-优化-Gemini-GPT`.

## Best candidates

These nodes completed compact `3/3` and averaged under 1 second:

| Node | Compact | Avg | Max |
| --- | ---: | ---: | ---: |
| 日本JP-A | 3/3 | 0.360s | 0.526s |
| 香港HK-A-Gemini | 3/3 | 0.540s | 0.696s |
| 新加坡-优化2-Gemini-GPT | 3/3 | 0.654s | 0.718s |
| 越南VN-A | 3/3 | 0.684s | 0.894s |
| 香港WAP-优化-Gemini | 3/3 | 0.697s | 0.729s |
| 新加坡-优化-Gemini-GPT | 3/3 | 0.793s | 0.800s |
| 美国USLA-A | 3/3 | 0.964s | 1.579s |
| 新加坡-优化3-Gemini | 3/3 | 0.979s | 1.636s |

Recommended first choices for long Codex sessions:

1. `日本JP-A`
2. `香港HK-A-Gemini`
3. `新加坡-优化2-Gemini-GPT`
4. `香港WAP-优化-Gemini`
5. `新加坡-优化-Gemini-GPT`

## Usable but slower

These nodes completed compact `3/3`, but the average was 1-2 seconds:

| Node | Avg |
| --- | ---: |
| 日本-优化 | 1.085s |
| 日本-优化2 | 1.339s |
| 香港-优化3-Gemini | 1.358s |
| 台湾-优化 | 1.507s |
| 印度-优化 | 1.670s |
| 香港WAP-优化3-Gemini | 1.736s |
| 乌克兰UA-A | 1.757s |
| 台湾-优化3 | 1.765s |
| 香港WAP-优化2-Gemini | 1.804s |

These are acceptable fallback nodes but less attractive than the sub-second group.

## Avoid for compact

Partial nodes had at least one compact timeout or SSL failure:

| Node | Compact | Main failure |
| --- | ---: | --- |
| 香港-优化-Gemini | 2/3 | SSL handshake timeout |
| 美国LA-优化2-GPT | 2/3 | SSL handshake timeout |
| 美国LA-优化3-GPT | 2/3 | SSL handshake timeout |
| 加拿大-优化2 | 2/3 | SSL handshake timeout |
| 香港-优化2-Gemini | 1/3 | SSL EOF |

Bad nodes failed compact `0/3`:

| Node | Main failure |
| --- | --- |
| 日本JP-HY2 | SSL EOF |
| 新加坡SG-HY2 | SSL EOF |
| 香港HK-HY2 | SSL EOF |
| 韩国KR-HY2 | SSL EOF |
| 德国DE-HY2 | SSL EOF |
| 新加坡SG-A-Gemini | SSL EOF |
| 俄罗斯RU-A | HTTP 403 |
| 土耳其TR-A | HTTP 403 |

## Conclusion

For this machine and this WiFi, Codex compact instability is not caused by official OpenAI auth because the active Codex path is the relay API at `www.fhl.mom`.

The practical fix is to keep Codex on a proven TCP/TLS node rather than HY2/Hysteria. HY2 nodes still fail consistently on this WiFi with SSL EOF symptoms, matching the earlier Hysteria finding.
