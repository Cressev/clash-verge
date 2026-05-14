# Official compact payload soak on zphz WiFi

Date: 2026-05-14

Scope:
- Network: zphz WiFi
- Target: `https://chatgpt.com/backend-api/codex/responses/compact`
- Request body: JSON payload with about 64 KiB of input text
- Success signal: official HTTP `401`, because this machine is not authenticated to official ChatGPT
- Failure signal: SSL EOF, SSL handshake timeout, read timeout
- Raw results:
  - `/tmp/official-compact-soak-candidates-20260514-114337.json`
  - `/tmp/official-compact-soak-more-candidates-20260514-121041.json`

## Why this test replaced the empty-body probe

The earlier empty-body official compact probe only showed that a node could reach the official endpoint. It did not model automatic compact well enough.

The user reported that `新加坡-优化-Gemini-GPT` still fails during real automatic compact. A larger payload soak reproduced that: the node reached only `15/25`, with 10 failures.

## Best replacements found

These nodes completed the larger-payload compact-like soak with no failures and no run at or above 4 seconds:

| Node | Result | Avg | Max | Slow >=4s |
| --- | ---: | ---: | ---: | ---: |
| 越南VN-A | 12/12 | 2.292s | 2.546s | 0 |
| 乌克兰UA-A | 12/12 | 2.353s | 2.560s | 0 |
| 新加坡-优化2-Gemini-GPT | 12/12 | 2.354s | 2.679s | 0 |

Recommended order:

1. `越南VN-A`
2. `新加坡-优化2-Gemini-GPT`
3. `乌克兰UA-A`

`德国-优化2` also reached `12/12`, but had one 6.735s spike, so it is a fallback rather than a first choice.

## User-reported failing node reproduced

| Node | Result | Failures | Main errors |
| --- | ---: | ---: | --- |
| 新加坡-优化-Gemini-GPT | 15/25 | 10 | read timeout, SSL EOF |

Conclusion: remove `新加坡-优化-Gemini-GPT` from the recommended official compact list despite its earlier empty-body success.

## Other candidates from the first soak

| Node | Result | Failures | Notes |
| --- | ---: | ---: | --- |
| 印度-优化 | 20/25 | 5 | best success count in first batch, but many slow runs |
| 英国-优化-GPT | 19/25 | 6 | frequent slow runs |
| 德国-优化 | 18/25 | 7 | not reliable enough for automatic compact |
| 香港-优化-Gemini | 17/25 | 8 | initially looked good, then repeated EOF/timeouts |
| 美国LA-优化2-GPT | 17/25 | 8 | repeated EOF/timeouts |
| 加拿大-优化2 | 14/25 | 11 | not reliable enough |
| 日本-优化 | 14/25 | 11 | not reliable enough |
| 日本-优化3 | 12/25 | 13 | not reliable enough |
| 日本-优化2 | 10/25 | 15 | not reliable enough |

## Other candidates from the second soak

| Node | Result | Failures | Notes |
| --- | ---: | ---: | --- |
| 德国-优化2 | 12/12 | 0 | fallback; one 6.735s spike |
| 加拿大-优化 | 11/12 | 1 | one initial read timeout, then stable |
| 台湾-优化2-GPT | 9/12 | 3 | EOF/read timeout |
| 香港WAP-优化-Gemini | 9/12 | 3 | slow and timeout-prone |
| 尼日利亚NG-A | 8/12 | 4 | EOF-prone |
| 香港HK-A-Gemini | 7/12 | 5 | EOF/read timeout |
| 日本JP-A | 7/12 | 5 | EOF/read timeout |
| 新加坡SG-A-Gemini | 7/12 | 5 | EOF/read timeout |
| 美国LA-优化3-GPT | 6/12 | 6 | not reliable enough |
| 香港HKT-A | 5/12 | 7 | not reliable enough |

## Conclusion

For automatic compact on zphz WiFi while HY2 is unavailable, the best replacement candidates found are `越南VN-A`, `新加坡-优化2-Gemini-GPT`, and `乌克兰UA-A`.

The earlier empty-body reachability result should not be used to choose compact nodes. It misses the EOF and read-timeout failures that appear with compact-like payloads.
