# 08. Windows + SSH Path

## 结论

Windows 上的关键是把飞连、Clash Verge TUN、SSH 的职责切清楚。

## 判断目标

SSH 真正连接的是：

```text
jumpserver.zphz.cn:2222
```

不要只盯着 `User` 字段里的内网 IP。

## 检查顺序

1. `nslookup jumpserver.zphz.cn`
2. 看 `profiles.yaml`
3. 看当前 `rules` 文件
4. 看当前 `merge` 文件里的 `route-exclude-address`
5. 必要时 `ssh -vvv zhipu30`

## 经验

如果公司域名进入 fake-ip，或者路由被 TUN 接管，SSH 表面上“像是连不上”，本质可能是 DNS 和路由没同时对齐。
