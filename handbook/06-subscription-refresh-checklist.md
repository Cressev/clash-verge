# 06. Subscription Refresh Checklist

订阅更新后，最容易变的是当前 profile 绑定的 `rules` 和 `merge` 文件。

## 最小检查

1. 看 `profiles.yaml` 里的 `current`、`rules`、`merge`。
2. 看 `dns_config.yaml` 里的 DNS 修复是否还在。
3. 看当前 `rules` 文件里公司域名、飞连进程和内网网段是否还在。
4. 看当前 `merge` 文件里 `route-exclude-address` 是否还在。
5. 完全退出并重启 Clash Verge。

## 验证命令

```powershell
Get-Content "$env:APPDATA\io.github.clash-verge-rev.clash-verge-rev\profiles.yaml" -TotalCount 250
Get-Content "$env:APPDATA\io.github.clash-verge-rev.clash-verge-rev\dns_config.yaml" -TotalCount 120
nslookup jumpserver.zphz.cn
```

## 经验

只要订阅一变，就别默认修复还在。先查当前 profile 绑定的文件，再决定补哪里。
